from flask import Flask, request
import pandas as pd
import numpy as np
import os
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import openpyxl
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

app = Flask(__name__)

# ********** SECURE LOGIN **********
@app.route('/securelogin/<UserID>/<Passcode>')
def securelogin(UserID, Passcode):
    fname = 'credential.csv'
    if not os.path.exists(fname):
        return "Error: Credential file not found. Please register first."

    data = pd.read_csv(fname, dtype=object)  # Read as object to handle mixed types
    for col in data.columns:
        if (data[col].dtype == object):
            data[col] = data[col].str.strip()

    return "Login Successful" if ((data['UserID'] == UserID) & (data['Passcode'] == Passcode)).any() else "Login Failed"

# ********** REGISTER NEW USER **********
@app.route('/register', methods=['POST'])
def register():
    UserID, Passcode = request.form['UserID'].strip(), request.form['Passcode'].strip()

    if not os.path.exists('credential.csv'):
        with open('credential.csv', 'w', newline='') as f:
            csv.writer(f).writerow(['UserID', 'Passcode'])

    data = pd.read_csv('credential.csv', dtype=object) #object type.
    for col in data.columns:
        if (data[col].dtype == object):
            data[col] = data[col].str.strip()

    if UserID in data['UserID'].values:
        return "UserID already exists."

    with open('credential.csv', 'a', newline='') as f:
        csv.writer(f).writerow([UserID, Passcode])

    return "Registration Successful"

# ********** FUNCTION TO SAVE DATA TO EXCEL **********
def save_data_to_excel(Age, moisture, humus, temp, humidity, waterrequired, fname):
    try:
        if not os.path.exists(fname):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(['Ageofplant', 'soilmoisture', 'soilhumus', 'temprature', 'humidity', 'waterrequired'])
            workbook.save(fname)

        wb = openpyxl.load_workbook(fname)
        sheet = wb.active
        sheet.append([Age, moisture, humus, temp, humidity, waterrequired])
        wb.save(fname)
        return "Data inserted successfully"
    except PermissionError:
        return f"Error: File '{fname}' is open. Close it and try again."
    except Exception as e:
        return f"Insertion failed: {str(e)}"

# ********** FUNCTION TO TRAIN & PREDICT **********
def train_and_predict(file, age, moisture, humus, temp, humidity):
    try:
        df = pd.read_excel(file)
        df = df.dropna()
        if len(df) < 10:
            return None, None, f"Error: Not enough data in '{file}' to train properly."

        features = ["Ageofplant", "soilmoisture", "soilhumus", "temprature", "humidity"]
        target = "waterrequired"

        X = df[features]
        Y = df[target]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = RandomForestRegressor(n_estimators=100, max_depth=8, min_samples_split=20, random_state=42)
        model.fit(X_train_scaled, Y_train)

        Y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(Y_test, Y_pred)
        rmse = np.sqrt(mse)

        input_data = pd.DataFrame([[age, moisture, humus, temp, humidity]], columns=features)
        input_scaled = scaler.transform(input_data)

        # Wheat Specific Logging (Debugging)
        if file == "wheatdataset.xlsx":
            print("Wheat Dataset Debugging:")
            print("  Input Data (Scaled):", input_scaled)
            prediction = model.predict(input_scaled)[0]
            print("  Prediction (Raw):", prediction)
        else:
            prediction = model.predict(input_scaled)[0]

        save_status = save_data_to_excel(age, moisture, humus, temp, humidity, prediction, file)

        print(f"Train and Predict - {file}:")
        print(f"  Prediction: {prediction}")
        print(f"  RMSE: {rmse}")
        print(f"  Save Status: {save_status}")
        return prediction, rmse, save_status
    except Exception as e:
        print(f"Error in train_and_predict ({file}): {str(e)}")
        return None, None, f"Error during training/prediction: {str(e)}"


# ********** PREDICT WATER DEMAND **********
@app.route('/predict_water/<Age>/<moisture>/<humus>/<temp>/<Humidity>/<num_plants>/<area_size>/<unit>')
def predict_water(Age, moisture, humus, temp, Humidity, num_plants, area_size, unit):
    try:
        Age, moisture, humus, temp, Humidity = map(float, [Age, moisture, humus, temp, Humidity])
        num_plants = int(num_plants)
        area_size = float(area_size)

        if unit == 'sqft':
            area_acres = area_size / 43560.0
        else:
            area_acres = area_size

        response = ""
        print("Area Size:", area_size)
        print("unit : ", unit)
        print("Area Acres:", area_acres)

        for crop in ['wheat', 'maize', 'pulse']:
            try:
                file = f"{crop}dataset.xlsx"
                prediction, rmse, save_status = train_and_predict(file, Age, moisture, humus, temp, Humidity)

                if prediction is not None:
                    water_demand_per_plant = prediction
                    if area_acres > 0:
                        water_demand_per_acre = prediction * num_plants / area_acres
                        water_demand_per_sqft = prediction * num_plants / area_size if area_size > 0 else 0 # Liters per sqft
                    else:
                        water_demand_per_acre = 0
                        water_demand_per_sqft = 0
                    response += f"{prediction},{water_demand_per_acre},{water_demand_per_sqft}\n" # added liters per sqft
                else:
                    response += f"-1,-1,-1\n" # Added -1 for liters per sqft
            except Exception as e:
                print(f"Error in {crop} model: {str(e)}")
                response += f"-1,-1,-1\n"
        print("Response after loop:", response)
        print("Water demand per acre: ", water_demand_per_acre)
        return response

    except Exception as e:
        print(f"Error in predict_water: {str(e)}")
        return f"Error: {str(e)}"



# ********** RUN FLASK APP **********
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)