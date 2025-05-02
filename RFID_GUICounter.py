import threading
import sys
import tkinter as tk
from collections import deque
import time

tags = deque()
flag = 0
tag_time = time.time()

def get_water_level():
    def update():
        global flag
        if 'ECAE34' in tags:
            waterLevel = str(0)
        elif 'ECB3CB' in tags:
            waterLevel = str(25)
        elif 'ECEFAB' in tags:
            waterLevel = str(50)
        elif 'ECDD59' in tags:
            waterLevel = str(75)
        elif 'EC3B21' in tags and flag == 1:
            waterLevel = str(100)
        else:
            waterLevel = str(100)

        clock.config(text=f"Water Level: {waterLevel}%")
        root.after(1000, update)

    root.after(1000, update)

def start_rfid_thread():
    threading.Thread(target=check_input_timeout, daemon=True).start()

def check_input_timeout():
    global flag, tag_time
    while True:
        if time.time() - tag_time > 10:
            flag = 1
        else:
            flag = 0
        time.sleep(1)

root = tk.Tk()
root.geometry("300x150")
root.title("Bucket Water Level")

clock = tk.Label(root, text="Water Level: N/A", font=("Arial", 20), fg="blue")
clock.pack(pady=20)

entry = tk.Entry(root, width=20)
entry.pack(pady=10)
entry.focus_set()

def on_tag_enter(event):
    global tag_time
    tag = entry.get().strip()
    tag_time = time.time()

    for i in range(len(tag) // 24):
        parsed = tag[i*24:(i+1)*24][18:24] # Extract the last 6 characters of each 24-character RFID tag
        if len(tags) >= 25:
            tags.popleft()
        tags.append(parsed)

    entry.delete(0, tk.END)  # clear box after processing

entry.bind("<Return>", on_tag_enter) # Bind the Return key to the on_tag_enter function

entry.bind("<Escape>", lambda event: root.quit()) # Bind the Escape key to quit the application

start_rfid_thread()
get_water_level()
root.mainloop()
