# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 13:27:56 2025

@author: DELL
"""

import time
import threading
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock App")
        self.time_format = 24  # Default 24-hour format
        
        self.label = tk.Label(root, text="", font=("Helvetica", 24))
        self.label.pack(pady=10)
        
        self.alarm_time = None
        self.countdown_target = None
        
        self.clock_button = tk.Button(root, text="Clock Mode", command=self.show_clock)
        self.clock_button.pack()
        
        self.alarm_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.alarm_button.pack()
        
        self.countdown_button = tk.Button(root, text="Countdown", command=self.set_countdown)
        self.countdown_button.pack()
        
        self.settings_button = tk.Button(root, text="Settings", command=self.change_format)
        self.settings_button.pack()
        
        self.update_clock()
    
    def update_clock(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M:%S %p" if self.time_format == 12 else "%H:%M:%S")
        self.label.config(text=current_time)
        self.check_alarm()
        self.root.after(1000, self.update_clock)
    
    def show_clock(self):
        messagebox.showinfo("Clock Mode", "Showing current time")
        self.update_clock()
    
    def set_alarm(self):
        self.alarm_time = simpledialog.askstring("Set Alarm", "Enter time (HH:MM, 24-hour format):")
        messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time}")
        
    def check_alarm(self):
        now = datetime.datetime.now().strftime("%H:%M")
        if self.alarm_time and now == self.alarm_time:
            messagebox.showinfo("Alarm", "Time's up!")
            self.alarm_time = None
    
    def set_countdown(self):
        target_time = simpledialog.askstring("Countdown", "Enter time (HH:MM, 24-hour format):")
        if target_time:
            now = datetime.datetime.now()
            target = datetime.datetime.strptime(target_time, "%H:%M")
            target = now.replace(hour=target.hour, minute=target.minute, second=0)
            if target < now:
                target += datetime.timedelta(days=1)
            self.countdown_target = target.timestamp()
            threading.Thread(target=self.run_countdown, daemon=True).start()
    
    def run_countdown(self):
        while self.countdown_target:
            remaining = int(self.countdown_target - time.time())
            if remaining <= 0:
                messagebox.showinfo("Countdown", "Countdown finished!")
                self.countdown_target = None
                break
            self.label.config(text=f"Countdown: {remaining} sec")
            time.sleep(1)
    
    def change_format(self):
        self.time_format = 12 if self.time_format == 24 else 24
        messagebox.showinfo("Settings", f"Time format set to {self.time_format}-hour mode")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()