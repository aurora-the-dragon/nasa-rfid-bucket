import tkinter as tk
from collections import deque
import threading

def recieve_tag_data():
    global tags

    while True:
        tag = input() 
        for i in range(len(tag) // 24):
            tag = tag[i*24:(i+1)*24][18:24]  # Extract the last 6 characters of each 24-character RFID tag
           # if len(tags) >= 50:
            get_water_level(tag)
            counter()
           #     tags.popleft()  # keep buffer of 50 tags
            tags.append(tag)
        tags.clear()

def get_water_level(tag):
    # Use results of tags to determine water level
    global waterLevel

    if 'ECAE34' in tag:
        waterLevel = str(10)
    elif 'ECB3CB' in tag:
        waterLevel = str(33)
    elif 'ECEFAB' in tag:
        waterLevel = str(66)
    elif 'ECDD59' in tag:
        waterLevel = str(99)
    else: # experimenting with full tag
        waterLevel = str(0)

   # print("The water level is " + waterLevel + "%")
   # clock.config(text=f"Water Level: {waterLevel}%")

def counter():
    global outlevel
    global count
    global waterLevel

    if waterLevel <= outlevel:
        outlevel = waterLevel
        count = 0
    elif count >= 50:
        outlevel = waterLevel
        count = 0
    else:
        count += 1

    countstr = str(count)
    print("count is " + countstr)
    print("The water level is " + outlevel + "%")
    print("The last read level is " + waterLevel + "%")
    clock.config(text=f"Water Level: {outlevel}%")

def start_rfid_thread():
    # seperate thread to process rfid tag info
    thread = threading.Thread(target=recieve_tag_data, daemon=True)
    thread.start()

# Initialize GUI
root = tk.Tk()
root.geometry("300x150")
root.title("Bucket Water Level")
clock = tk.Label(root, text="Water Level: N/A", font=("Arial", 20), fg="blue")
clock.pack(pady=20)

outlevel = str(80)
waterlevel = str(80)
count = 0

tags = deque()
start_rfid_thread()
root.mainloop()