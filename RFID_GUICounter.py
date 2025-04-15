import threading
import select
import sys
import tkinter as tk
from collections import deque
import time

def recieve_tag_data():
    global tags
    while True:
        tag = input() 
        
        global tag_time
        tag_time = time.time()

        for i in range(len(tag) // 24):
            tag = tag[i*24:(i+1)*24][18:24]  # Extract the last 6 characters of each 24-character RFID tag
            if len(tags) >= 25:
                tags.popleft()  # keep buffer of 100 tags
            tags.append(tag)

def get_water_level():
    while True:
        time.sleep(1)  # sleep for 1 s to prevent CPU overload
        if 'ECAE34' in tags:
            waterLevel = str(0)
        elif 'ECB3CB' in tags:
            waterLevel = str(25)
        elif 'ECEFAB' in tags:
            waterLevel = str(50)
        elif 'ECDD59' in tags:
            waterLevel = str(75)
        elif 'EC3B21' and flag == 1:
            waterLevel = str(100)
        else: 
            waterLevel = str(100)

        print("The water level is " + waterLevel + "%")
        clock.config(text=f"Water Level: {waterLevel}%")

def start_rfid_thread():
    # seperate thread to process rfid tag info
    thread1 = threading.Thread(target=recieve_tag_data, daemon=True)
    thread1.start()
    thread2 = threading.Thread(target=check_input_timeout, daemon=True)
    thread2.start()
    thread3 = threading.Thread(target=get_water_level, daemon=True)
    thread3.start()

def check_input_timeout():
    global flag
    global tag_time
    tag_time = time.time()
    while True:
        time_check = time.time()
        if time_check - tag_time > 10:
            #print("No input received for 10 seconds, setting flag to 1")
            flag = 1
        else:
            flag = 0  # reset flag if input is received

# Initialize GUI
root = tk.Tk()
root.geometry("300x150")
root.title("Bucket Water Level")
clock = tk.Label(root, text="Water Level: N/A", font=("Arial", 20), fg="blue")
clock.pack(pady=20)

tags = deque()
start_rfid_thread()
root.mainloop()
