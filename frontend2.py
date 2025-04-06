# ******************Water Demand Prediction in an agriculture field for the primary crop using machine learning*********************************************************************************

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

fapp = Tk()
fapp.state('zoomed')
fapp.title("Water Demand Prediction for Primary Crop")
fapp.configure(bg="#1E1E1E")

# Create a canvas to draw the gradient background///////////////////////////////

def create_gradient(canvas, width, height, start_color, end_color):
    """ Creates a vertical gradient from start_color to end_color """
    for i in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / height))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color, width=1)


canvas = Canvas(fapp, width=1700, height=800)
canvas.place(x=0, y=0)

# Define gradient start and end colors
start_color = (0, 0, 139)  # Dark Blue
end_color = (0, 255, 255)  # Cyan

# Draw the gradient on the canvas
create_gradient(canvas, 1700, 800, start_color, end_color)

# ******************************************************************OUTPUT FRAME****************************************************************************************************************

def tent_output():
    global r_frame, t_frame
    if 'value' not in globals():
        messagebox.showerror("Error", "Prediction data is missing. Run prediction first.")
        return

    # Forgetting the r_frame if it exists
    if r_frame is not None:
        r_frame.place_forget()

    # Creating the t_frame for displaying text analysis
    t_frame = Frame(fapp, bg='black', relief="ridge", bd=7)
    t_frame.place(x=250, y=80, height=650, width=1000)

    # Creating an inner frame for better organization
    out_frame = Frame(t_frame, relief="ridge", bg='black', bd=5)
    out_frame.place(x=110, y=150, height=390, width=800)

    # Displaying the title for the text analysis section
    Label(t_frame, text='The Water Prediction Result', bg='white', fg='black', font=('georgia', 35, 'bold')).place(x=150, y=50)

    # Displaying labels and entry fields for each crop's water demand prediction
    crops = ['Wheat', 'Maize', 'Pulse']
    y_offset = 50  # Starting Y-coordinate for the first crop

    for i, crop in enumerate(crops):
        # Crop name label
        Label(out_frame, text=crop, font=('georgia', 25), bg='black', fg='white', highlightthickness=3, highlightbackground='black', highlightcolor='black').place(x=90, y=y_offset)

        # Entry field to display the predicted value

        entry_per_plant = Entry(out_frame, highlightthickness=3, highlightcolor='black')
        entry_per_plant.place(x=230, y=y_offset + 2, height=40, width=70)
        Label(out_frame, text='Liters/Plant', font=('georgia', 10)).place(x=310, y=y_offset + 16)

        entry_per_sqft = Entry(out_frame, highlightthickness=3, highlightcolor='black')
        entry_per_sqft.place(x=440, y=y_offset + 2, height=40, width=70)
        Label(out_frame, text='Liters/SqFt', font=('georgia', 10)).place(x=515, y=y_offset + 16)

        entry_per_acre = Entry(out_frame, highlightthickness=3, highlightcolor='black')
        entry_per_acre.place(x=630, y=y_offset + 2, height=40, width=70)
        Label(out_frame, text='Liters/Acre', font=('georgia', 10)).place(x=705, y=y_offset + 16)

        
        # Populate the entry fields with the predicted values
        if i < len(value):  # Ensure there is a corresponding value for the crop
            per_plant, per_acre, per_sqft = map(float, str(value[i]).replace('(', '').replace(')', '').split(','))
            entry_per_plant.insert(0, str(per_plant))  # Insert the predicted value per plant
            entry_per_acre.insert(0, str(per_acre))  # Insert the predicted value per area
            entry_per_sqft.insert(0, str(per_sqft)) # Insert the predicted value per sqft

        y_offset += 90  # Increment Y-coordinate for the next crop

    # Buttons for navigation
    Button(t_frame, text='Home', bg='green', fg='white', font=('georgia', 20), command=ready).place(x=450, y=550, height=50, width=100)
    Button(t_frame, text='Graph Analysis', bg='royalblue', fg='white', font=('georgia', 20), command=result).place(x=580, y=550, height=50, width=200)
    
    
# ***************************************************************BAR GRAPH**********************************************************************************************************************

def result():
    global r_frame, name, value
    if 'name' not in globals() or 'value' not in globals():
        messagebox.showerror("Error", "Prediction data is missing. Run prediction first.")
        return
    
    if d_frame:
        d_frame.place_forget()
    else:
        print("No d_frame")
    
    r_frame = Frame(fapp, bg='black', relief="ridge",bd = 7)
    r_frame.place(x=250, y =80, height = 650, width = 1000)

    Label(r_frame, text = 'Predicted Result', font = ('georgia', 30,'bold'), fg = 'black', bg = 'white').place(x=350, y=50)
    
    bar_frame = Frame(r_frame, relief="ridge",bg = 'black', bd=5)
    bar_frame.place(x=110, y=150, height = 390, width = 800) 
    
    Button(r_frame, text = 'Home', bg = 'green', fg = 'white',font=('georgia',20) ,command = ready).place(x=450, y=550, height = 50, width = 100)
    Button(r_frame, text = 'Text Analysis', bg = 'royalblue', fg = 'white',font=('georgia',20), command = tent_output).place(x=580, y=550, height = 50, width = 180)
    
    # Graph plot --------------------------------------------------------------
    fig, ax = plt.subplots()
    colors = ['red','lightgreen','blue']
    ax.bar(name, [float(v[0]) for v in value], color = colors)
    ax.set_xlabel('\n ------------ Crops ------------')
    ax.set_ylabel('------------ Water Demand (Liters/Plant) ------------')
    ax.set_title('Predicted Water Demand')
    canvas = FigureCanvasTkAgg(fig, master=bar_frame)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    
# Prediction of Primary Crop by getting the user input-------------------------

def Predict_PC():
    global s, name, value

    messagebox.showinfo("Processing", "Loading Please wait........")
    Age = Ageofplant.get()
    moisture = soilmoisture.get()
    humus = soilhumus.get()
    temp = temprature.get()
    Humidity = humidity.get()
    num_plants = num_plants_entry.get()
    area_size = area_size_entry.get()
    unit = unit_var.get()

    print("Input Data:", Age, moisture, humus, temp, Humidity, num_plants, area_size, unit)
    print("Unit Value:", unit_var.get())
    
    # Basic input validation
    try:
        float(Age), float(moisture), float(humus), float(temp), float(Humidity), int(num_plants), float(area_size)
    except ValueError:
        messagebox.showerror("Error", "Please enter numerical values for all fields.")
        return False

    url = f"http://127.0.0.1:5000/predict_water/{Age}/{moisture}/{humus}/{temp}/{Humidity}/{num_plants}/{area_size}/{unit}"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        prediction_result = response.text
        print("API Response:", prediction_result)

        s = prediction_result.splitlines()
        print("Split Lines:", s)

        if len(s) == 3:
            try:
                wheat_demand = tuple(map(float, s[0].strip().split(',')))
                maize_demand = tuple(map(float, s[1].strip().split(',')))
                pulse_demand = tuple(map(float, s[2].strip().split(',')))

                if wheat_demand[0] == -1 or maize_demand[0] == -1 or pulse_demand[0] == -1:
                    messagebox.showerror("Error", "Prediction failed for one or more crops.")
                    return False

                name = ["Wheat", "Maize", "Pulse"]
                value = [wheat_demand, maize_demand, pulse_demand]
                print("Prediction Success")
                return True

            except ValueError:
                messagebox.showerror("Error", "Error parsing prediction data.")
                return False
        else:
            messagebox.showerror("Error", "Unexpected response from server.")
            return False
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request error: {e}")
        return False
    except Exception as e:
        print(f"Frontend error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return False
    
    
    for item in s:
        print(item)
    
    if len(s) >= 4:
        try:
            print("Response Strings:") # Added lines
            if len(s) > 1:
                print(s[1])
                wheat_demand = int(s[1].split(":")[1].split(",")[0].strip())
            else:
                wheat_demand = None
    
            if len(s) > 2:
                print(s[2])
                maize_demand = int(s[2].split(":")[1].split(",")[0].strip())
            else:
                maize_demand = None
    
            if len(s) > 3:
                print(s[3])
                pulse_demand = int(s[3].split(":")[1].split(",")[0].strip())
            else:
                pulse_demand = None
    
            if wheat_demand is not None and maize_demand is not None and pulse_demand is not None:
                print("Wheat Demand:", wheat_demand)
                print("Maize Demand:", maize_demand)
                print("Pulse Demand:", pulse_demand)
    
                first = wheat_demand
                second = maize_demand
                third = pulse_demand
                print(first, second, third)
                name = ["Wheat", "Maize", "Pulse"]
                value = [first, second, third]
                return True
            else:
                messagebox.showerror("Error", "Error parsing prediction data.")
                return False
    
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Error parsing data: {e}")
            return False
    else:
        messagebox.showerror("Error", "Unexpected response from server.")
        return False
    
    
# Predict button does 2 functions ------------------------------
# 1. It predicts the Output and saves the data.
# 2. It forgets the d_frame & moves to next frame.

def do_predict():
    if Predict_PC():
        result()
    

# *************************************************************PREDICTION OF WATER REQUIRED FOR CROP*******************************************************************************************
      
def predict():
    
    global d_frame
    
    global Ageofplant, soilmoisture, soilhumidity, soilhumus, temprature, humidity, num_plants_entry, area_size_entry, unit_var
    
    if l_frame:
        l_frame.place_forget()
    
    d_frame = Frame(fapp, bg = '#1a1a2e',padx=40, pady=40, relief="ridge", bd=4)
    d_frame.place(x=250, y =80, height = 650, width = 1000)
     
    Label(d_frame, text = 'Water Prediction for Primary Crop', font = ('georgia',30,'bold'), fg='black', bg='white',padx=10, pady=5, relief="ridge", bd=2).place(x=160, y=10)

    Label(d_frame, text = 'Age of Plant', font=('georgia',20), bg = '#1a1a2e', fg = 'white').place(x=110, y=100)
    Ageofplant = Entry(d_frame,bg="#e0e0e0", bd=2, relief='ridge', width=50)
    Ageofplant.place(x=340, y=100, height = 30, width = 100)
    Label(d_frame, text = 'days', font=('georgia',10), bg = '#1a1a2e', fg = 'white').place(x=440, y=110)
   
    Label(d_frame, text = 'Soil Moisture', font=('georgia',20), bg = '#1a1a2e', fg = 'white').place(x=110, y=160)
    soilmoisture = Entry(d_frame,bg="#e0e0e0",bd=2, relief='ridge', width=50)
    soilmoisture.place(x=340, y=160, height = 30, width = 100)
    Label(d_frame, text = 'VWC[%]', font=('georgia',10), bg = '#1a1a2e', fg = 'white').place(x=440, y=170)
       
    Label(d_frame, text = 'Soil Humus', font=('georgia',20), bg = '#1a1a2e', fg = 'white').place(x=110, y=220)
    soilhumus = Entry(d_frame,bg="#e0e0e0",bd=2, relief='ridge', width=50)
    soilhumus.place(x=340, y=220, height = 30, width = 100)
    Label(d_frame, text = '%', font=('georgia',10), bg = '#1a1a2e', fg = 'white').place(x=440, y=230)

    Label(d_frame, text = 'Temprature', font=('georgia',20), bg = '#1a1a2e', fg = 'white').place(x=110, y=280)
    temprature = Entry(d_frame,bg="#e0e0e0",bd=2, relief='ridge', width=50)
    temprature.place(x=340, y=280, height = 30, width = 100)
    Label(d_frame, text = '°F', font=('georgia',10), bg = '#1a1a2e', fg = 'white').place(x=440, y=290)

    Label(d_frame, text = 'Humidity', font=('georgia',20), bg = '#1a1a2e', fg = 'white').place(x=110, y=340)
    humidity = Entry(d_frame,bg="#e0e0e0",bd=2, relief='ridge', width=50)
    humidity.place(x=340, y=340, height = 30, width = 100)
    Label(d_frame, text = '%RH', font=('georgia',10), bg = '#1a1a2e', fg = 'white').place(x=440, y=350)
    
    Label(d_frame, text = 'Number of Plants', font=('georgia',20), bg = '#1a1a2e', fg = 'white').place(x=110, y=400)
    num_plants_entry = Entry(d_frame,bg="#e0e0e0",bd=2, relief='ridge', width=50)
    num_plants_entry.place(x=340, y=400, height = 30, width = 100)
    Label(d_frame, text = 'plants', font=('georgia',10), bg = '#1a1a2e', fg = 'white').place(x=440, y=410)
    
    Label(d_frame, text = 'Area Size', font=('georgia',20), bg = '#1a1a2e', fg = 'white').place(x=110, y=460)
    area_size_entry = Entry(d_frame,bg="#e0e0e0",bd=2, relief='ridge', width=50)
    area_size_entry.place(x=340, y=460, height = 30, width = 100)
    #Label(d_frame, text = 'acres', font=('georgia',10), bg = '#1a1a2e', fg = 'white').place(x=440, y=470)
      
    # Option menu for unit selection ----------
    unit_var = StringVar(d_frame)
    unit_var.set("acres")  # default value
    unit_menu = OptionMenu(d_frame, unit_var, "acres", "sqft")
    unit_menu.place(x=440, y=460, height=30, width=100)
    
    predict_btm = Button(d_frame, text = 'Predict', bg = 'royalblue', fg = 'white', font=('georgia', 20), activebackground='#0052cc', bd=3, relief='raised', command = do_predict).place(x=780, y=480, height = 50, width = 100) 
    

# Function to handle New User Registration
def register_user():
    def submit_registration():
        name = name_entry.get()
        dob = dob_entry.get()
        age = age_entry.get()
        contact = contact_entry.get()
        email = email_entry.get()
        userid = userid_entry.get()
        passcode = pass_entry.get()
        confirm_passcode = confirm_passcode_entry.get()

        if passcode != confirm_passcode:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not all([userid, passcode, name, dob, age, contact, email]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            url = "http://127.0.0.1:5000/register"
            data = {
                "Name": name,
                "Age": age,
                "DOB": dob,
                "Contact": contact,
                "UserID": userid,
                "Passcode": passcode,
                "Confirm Passcode": confirm_passcode,
                "Email": email
            }
            response = requests.post(url, data=data)

            if response.status_code == 200 and response.text.strip() == "Registration Successful":
                messagebox.showinfo("Success", "Registration Successful!")
                register_window.destroy()
            else:
                messagebox.showerror("Error", response.text)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

    register_window = Toplevel(fapp)  # Use fapp instead of l_frame
    register_window.title("Registration")
    window_width = 600
    window_height = 600
    screen_width = fapp.winfo_screenwidth()
    screen_height = fapp.winfo_screenheight()

    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    register_window.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    # Use pack() consistently instead of grid()
    form_frame = Frame(register_window)
    form_frame.pack(pady=40, padx=40)

    Label(form_frame, text="Register Here", font=('georgia', 16)).pack(pady=2)

    Label(form_frame, text="Name").pack()
    name_entry = Entry(form_frame)
    name_entry.pack()

    Label(form_frame, text="Age").pack()
    age_entry = Entry(form_frame)
    age_entry.pack()

    Label(form_frame, text="DOB").pack()
    dob_entry = Entry(form_frame)
    dob_entry.pack()

    Label(form_frame, text="Contact").pack()
    contact_entry = Entry(form_frame)
    contact_entry.pack()

    Label(form_frame, text="Email").pack()
    email_entry = Entry(form_frame)
    email_entry.pack()

    Label(form_frame, text="Username").pack()
    userid_entry = Entry(form_frame)
    userid_entry.pack()

    Label(form_frame, text="Password").pack()
    pass_entry = Entry(form_frame, show="*")
    pass_entry.pack()

    Label(form_frame, text="Confirm Password").pack()
    confirm_passcode_entry = Entry(form_frame, show="*")
    confirm_passcode_entry.pack()

    # Submit button
    submit_button = Button(form_frame, text="Submit", command=submit_registration)
    submit_button.pack(pady=2)

        
        


def Login(event=None):
  userid = id_entry.get()
  passcode = pass_entry.get()
  
  if not userid or not passcode:
    messagebox.showerror("Error", "Please enter both UserId and Passcode.")
    return 0

  url = "http://127.0.0.1:5000/securelogin/"+userid+"/"+passcode  
  response = requests.get(url)
  print(response.text)
  print(response)
  if response.status_code == 200 and response.text.strip() == "Login Successful":
      messagebox.showinfo("Success","Login Successful !")
      predict()
  else:
      messagebox.showerror("Error","Login Failed !")
      


# l_frame Creation ------------------------------------------------------------

def ready():
    global l_frame, id_entry, pass_entry  
    
    if w_frame:
        w_frame.place_forget()
    else:
        print("w_frame not created")
        return  
    
    # Create login frame
    l_frame = Frame(fapp, bg='black', bd=5, relief="ridge")
    l_frame.place(x=250, y =80, height = 650, width = 1000)

    Label(l_frame, text='Secure Login', font=('georgia', 35, 'bold'), bg='white', fg='black').place(x=315, y=10)

    Label(l_frame, text='Agricultural \n UserID', font=('georgia', 30), bg='black', fg='white').place(x=160, y=150)
    id_entry = Entry(l_frame, highlightthickness=2, highlightbackground='black')
    id_entry.place(x=470, y=150, height=40, width=250)

    Label(l_frame, text='Passcode', font=('georgia', 30), bg='black', fg='white').place(x=160, y=280)
    pass_entry = Entry(l_frame, highlightthickness=2, highlightbackground='black', show="*")
    pass_entry.place(x=470, y=280, height=40, width=250)

    Button(l_frame, text='Login', bg='green', fg='white', font=('georgia', 20), command=Login).place(x=420, y=400, height=50, width=100)

    # Bind the return key only to the password entry
    pass_entry.bind('<Return>', Login)
    
    Label(l_frame, text = "Don't have a Account ? \n", font = ('georgia',20), bg = 'black', fg = 'white').place(x=320, y=450)
    new_user_button = Button(l_frame, text="Signup",bg='blue', fg='white', font=('georgia', 20), command=register_user)
    new_user_button.place(x=420, y=500)



# Main Website creation -------------------------------------------------------
# w_frame creation /////////////////////////////////////////////////

# Display the welcome frame of Project /////////////////////////////
w_frame = Frame(fapp, bg = 'black', relief = "ridge",bd = 5 )
w_frame.place(x=20, y =20, height = 750, width = 1500)

# Background image //////////////////////////////////////////////////
bg_img = Image.open("Crop_image.jpg")
bg_pht = ImageTk.PhotoImage(bg_img.resize((1500,750)))
bg_label = Label(w_frame, image = bg_pht)
bg_label.place(x=0 , y=0, relwidth = 1, relheight = 1)
bg_label.lower()

# Display the logo on the frame ////////////////////////////////////
image = Image.open('clg_logo.jpeg')
image.thumbnail((500, 500), Image.Resampling.LANCZOS)

# Display the image ///////////////////////////////////////////////
photo = ImageTk.PhotoImage(image)
p_label = Label(w_frame, image = photo, highlightthickness=2, highlightcolor='black', highlightbackground='black')
p_label.place(x=18,y=18)

# Display the title of the project ///////////////////////////////
label_bg = "C:/Users/MANASA N S/OneDrive/Desktop/final project/Backend/Frontend/Crop_image2.jpg"
if os.path.exists(label_bg):
    label_bg_im = Image.open(label_bg)
    label_bg_pht = ImageTk.PhotoImage(label_bg_im.resize((1380,120)))
    label = Label(w_frame, image = label_bg_pht, text = "Water Demand Prediction in an Agriculture field \n for the Primary Crop using Machine Learning", font=('georgia',40,'bold'), fg = 'black',compound="center")
    label.image = label_bg_im
    label.place(x=110, y=10, height = 120, width = 1380)
else:
    print("Warning")
    label = Label(w_frame,text = "Water Demand Prediction in an Agriculture field \n for the Primary Crop using Machine Learning",font = ('georgia',40,'bold'), bg = '#9BA6B7', fg = 'white').place(x=110, y=10, height = 120, width = 1395)

# Proceed button /////////////////////////////////////////////////
Button(w_frame, text = 'Proceed >', bg = 'royalblue', fg = 'white', font=('georgia',20) ,command = ready).place(x=1250, y=580, height = 50, width = 140)

# main loop for running the program ---------------------------
fapp.mainloop()
