import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition2023-default-rtdb.firebaseio.com/"
})


# Get reference to the database root
ref = db.reference()

# Create a tkinter window
root = tk.Tk()
root.title("Firebase Database")

# Create labels and entry boxes for data fields
tk.Label(root, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="designation").grid(row=2, column=0)
designation_entry = tk.Entry(root)
designation_entry.grid(row=2, column=1)

tk.Label(root, text="department").grid(row=3, column=0)
department_entry = tk.Entry(root)
department_entry.grid(row=3, column=1)

tk.Label(root, text="work_location").grid(row=4, column=0)
work_location_entry = tk.Entry(root)
work_location_entry.grid(row=4, column=1)

tk.Label(root, text="cnic").grid(row=5, column=0)
cnic_entry = tk.Entry(root)
cnic_entry.grid(row=5, column=1)

tk.Label(root, text="mobile").grid(row=6, column=0)
mobile_entry = tk.Entry(root)
mobile_entry.grid(row=6, column=1)


def add_data():
    # Get the data from the entry boxes
    id = id_entry.get()
    name = name_entry.get()
    designation = designation_entry.get()
    department = (department_entry.get())  # add entry for starting year
    work_location = (work_location_entry.get())  # add entry for total attendance
    cnic = cnic_entry.get()  # add entry for standing
    mobile = int(mobile_entry.get())  # add entry for year

    # Check if the ID already exists in the database
    student_ref = ref.child("Employees").child(id)
    if student_ref.get() is not None:
        # Ask the user if they want to update the existing data
        response = messagebox.askyesno("Update Data", "ID already exists. Do you want to update the data?")
        if not response:
            return
    data = {}

    if name:
        data["name"] = name

    if designation:
        data["designation"] = designation

    if department:
        data["department"] = department

    if work_location:
        data["work_location"] = work_location
    if cnic:
        data["cnic"] = cnic

    if mobile:
        data["mobile"] = int(mobile)

    # Update the data in Firebase database
    ref.child("Employees").child(id).update(data)
    result_label.config(text="Data added/updated successfully")

    # Update the data in Firebase database
    student_ref.update(data)
    result_label.config(text="Data added/updated successfully")


# Function to retrieve data from Firebase database
def retrieve_data():
    # Get the ID of the user to retrieve data for
    id = id_entry.get()

    # Check if the user exists in the database
    if ref.child("Employees").child(id).get() is None:
        result_label.config(text="User does not exist in the database")
    else:
        # Retrieve the user data from Firebase database
        user_data = ref.child("Employees").child(id).get()

        # Update the entry boxes with the retrieved data
        name_entry.delete(0, tk.END)
        name_entry.insert(0, user_data["name"])

        designation_entry.delete(0, tk.END)
        designation_entry.insert(0, user_data["designation"])

        department_entry.delete(0, tk.END)
        department_entry.insert(0, user_data["department"])

        work_location_entry.delete(0, tk.END)
        work_location_entry.insert(0, user_data["work_location"])

        cnic_entry.delete(0, tk.END)
        cnic_entry.insert(0, user_data["cnic"])

        mobile_entry.delete(0, tk.END)
        mobile_entry.insert(0, user_data["mobile"])

        result_label.config(text="Data retrieved successfully")

# Create a button to retrieve data
retrieve_button = tk.Button(root, text="Retrieve Data", command=retrieve_data)
retrieve_button.grid(row=7, column=0)

# Create a label to show the result message
result_label = tk.Label(root, text="")
result_label.grid(row=8, columnspan=2)


# Create a button to add or update data
add_button = tk.Button(root, text="Add/Update Data", command=add_data)
add_button.grid(row=7, column=1)

root.mainloop()
