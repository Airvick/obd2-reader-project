import obd
import time
from tkinter import Tk, Label, Button, StringVar, Frame

def connect_obd():
    global connection
    connection = obd.OBD()  # Automatically connects to the OBD-II adapter
    if connection.is_connected():
        status_var.set("Connected to OBD-II Adapter")
    else:
        status_var.set("Failed to connect")

def read_dtc():
    if connection.is_connected():
        cmd = obd.commands.GET_DTC  # Get Diagnostic Trouble Codes
        response = connection.query(cmd)
        if response.is_successful():
            dtc_list = "\n".join([f"Code: {code}" for code in response.value])
            output_var.set(f"Detected Trouble Codes:\n{dtc_list}")
        else:
            output_var.set("No trouble codes detected.")
    else:
        output_var.set("Not connected to OBD-II Adapter")

def read_rpm():
    if connection.is_connected():
        cmd = obd.commands.RPM  # Get engine RPM
        response = connection.query(cmd)
        if response.is_successful():
            output_var.set(f"Current RPM: {response.value}")
        else:
            output_var.set("Failed to read RPM")
    else:
        output_var.set("Not connected to OBD-II Adapter")

def clear_dtc():
    if connection.is_connected():
        cmd = obd.commands.CLEAR_DTC  # Clear Diagnostic Trouble Codes
        connection.query(cmd)
        output_var.set("Diagnostic Trouble Codes cleared.")
    else:
        output_var.set("Not connected to OBD-II Adapter")

# GUI Application
root = Tk()
root.title("OBD-II Reader")

frame = Frame(root)
frame.pack(pady=10)

status_var = StringVar()
status_var.set("Press 'Connect' to start")

output_var = StringVar()
output_var.set("")

status_label = Label(frame, textvariable=status_var, fg="blue")
status_label.pack()

output_label = Label(frame, textvariable=output_var, fg="green", wraplength=400, justify="left")
output_label.pack()

connect_button = Button(frame, text="Connect", command=connect_obd, width=20)
connect_button.pack(pady=5)

read_dtc_button = Button(frame, text="Read Trouble Codes", command=read_dtc, width=20)
read_dtc_button.pack(pady=5)

read_rpm_button = Button(frame, text="Read RPM", command=read_rpm, width=20)
read_rpm_button.pack(pady=5)

clear_dtc_button = Button(frame, text="Clear Trouble Codes", command=clear_dtc, width=20)
clear_dtc_button.pack(pady=5)

exit_button = Button(frame, text="Exit", command=root.quit, width=20)
exit_button.pack(pady=5)

root.mainloop()
