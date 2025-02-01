import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import time
import threading
import random

# Data lokasi contoh untuk Geo-Reminders
LOCATIONS = ["Supermarket"]

# Daftar motivasi
MOTIVATIONAL_QUOTES = [
    "You are capable of amazing things!",
    "Stay focused, stay strong!",
    "Small steps every day lead to big results.",
    "Believe in yourself, and anything is possible!"
]

# Variabel global untuk penghargaan dan waktu istirahat
task_completion_count = 0
break_time = 3600
non_productive_time = 0
remaining_time = break_time  # Untuk timer mundur
timer_running = False  # Status timer

# Fungsi untuk Geo-Reminders
def check_geo_reminder(user_location):
    user_location = user_location.strip().lower()
    for location in LOCATIONS:
        if user_location == location.lower().strip():
            messagebox.showinfo("Geo-Reminder", f"You're near {location}. Don't forget to visit!")
            return
    messagebox.showwarning("Geo-Reminder", "Location not found in the list.")

# Fungsi untuk menambahkan tugas rutin
def add_routine_task():
    task_name = task_entry.get()
    if task_name:
        routine_task_listbox.insert(tk.END, task_name)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task name cannot be empty!")

# Fungsi untuk menambahkan tugas non-rutin
def add_non_routine_task():
    details = task_details_text.get("1.0", tk.END).strip()
    if details:
        task = details  # Tidak ada file yang dilampirkan
        non_routine_task_listbox.insert(tk.END, task)
        task_details_text.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Input Error", "Task details cannot be empty!")

# Fungsi untuk menyelesaikan tugas
def complete_task():
    global task_completion_count, non_productive_time
    selected_task = routine_task_listbox.curselection() or non_routine_task_listbox.curselection()
    if selected_task:
        task_listbox = routine_task_listbox if routine_task_listbox.curselection() else non_routine_task_listbox
        task_listbox.delete(selected_task)
        task_completion_count += 1
        non_productive_time = 0  # Reset non-productive time on task completion
        messagebox.showinfo("Task Completed!", f"Well done! You’ve completed {task_completion_count} tasks.")
        if task_completion_count % 5 == 0:
            messagebox.showinfo("Reward Unlocked!", "Congratulations! You’ve earned a productivity badge!")
    else:
        messagebox.showwarning("Selection Error", "No task selected!")

# Fungsi untuk menambahkan lokasi baru
def add_location():
    new_location = new_location_entry.get().strip()
    if new_location:
        LOCATIONS.append(new_location)
        new_location_entry.delete(0, tk.END)
        messagebox.showinfo("Location Added", f"{new_location} has been added to the location list.")
    else:
        messagebox.showwarning("Input Error", "Location name cannot be empty!")

# Fungsi untuk pengingat waktu istirahat
def remind_break():
    global break_time, non_productive_time, remaining_time, timer_running
    while True:
        if timer_running and remaining_time > 0:
            time.sleep(1)
            remaining_time -= 1
            update_timer_label()
        elif timer_running and remaining_time <= 0:
            messagebox.showinfo("Break Reminder", "Time for a short break!")
            remaining_time = break_time  # Reset timer
            timer_running = False

# Fungsi untuk memperbarui tampilan timer mundur
def update_timer_label():
    minutes, seconds = divmod(remaining_time, 60)
    timer_label.config(text=f"Break Timer: {minutes:02}:{seconds:02}")

# Fungsi untuk menampilkan motivasi
def show_motivation():
    quote = random.choice(MOTIVATIONAL_QUOTES)
    messagebox.showinfo("Motivation Boost", quote)

# Fungsi untuk mengatur waktu istirahat
def set_break_time():
    global break_time, remaining_time
    try:
        new_time = int(break_time_entry.get()) * 60
        break_time = new_time
        remaining_time = break_time  # Reset remaining time saat mengubah break time
        break_time_entry.delete(0, tk.END)
        messagebox.showinfo("Break Time Updated", f"Break time set to {new_time // 60} minutes.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number!")

# Fungsi untuk memulai timer
def start_timer():
    global timer_running
    if not timer_running:
        timer_running = True

# Fungsi untuk menghentikan timer
def stop_timer():
    global timer_running
    if timer_running:
        timer_running = False

# Analisis waktu tidak produktif
def analyze_non_productive_time():
    global non_productive_time
    hours, remainder = divmod(non_productive_time, 3600)
    minutes, _ = divmod(remainder, 60)
    messagebox.showinfo("Non-Productive Time Analysis", f"You have spent {hours} hours and {minutes} minutes being non-productive. Consider improving your focus.")

# GUI
root = tk.Tk()
root.title("Time Management App")

# Scrollable Frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Tambahkan fungsi untuk scroll dengan mouse di mana saja
def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

root.bind("<MouseWheel>", on_mouse_wheel)

# Routine Tasks
tk.Label(scrollable_frame, text="Routine Tasks:").pack(pady=5)
routine_task_listbox = tk.Listbox(scrollable_frame, width=50, height=10)
routine_task_listbox.pack(pady=5)
tk.Label(scrollable_frame, text="Task Name:").pack(pady=5)
task_entry = tk.Entry(scrollable_frame, width=40)
task_entry.pack(pady=5)
tk.Button(scrollable_frame, text="Add Routine Task", command=add_routine_task).pack(pady=5)

# Non-Routine Tasks
tk.Label(scrollable_frame, text="Non-Routine Tasks:").pack(pady=5)
non_routine_task_listbox = tk.Listbox(scrollable_frame, width=50, height=10)
non_routine_task_listbox.pack(pady=5)
tk.Label(scrollable_frame, text="Non-Routine Task Details:").pack(pady=5)
task_details_text = tk.Text(scrollable_frame, width=40, height=4)
task_details_text.pack(pady=5)
tk.Button(scrollable_frame, text="Add Non-Routine Task", command=add_non_routine_task).pack(pady=5)

# Geo-Reminder Checker
tk.Label(scrollable_frame, text="Input Current Location:").pack(pady=5)
location_entry = tk.Entry(scrollable_frame, width=40)
location_entry.pack(pady=5)
tk.Button(scrollable_frame, text="Check Location", command=lambda: check_geo_reminder(location_entry.get())).pack(pady=5)

# Add New Location
tk.Label(scrollable_frame, text="Add New Location:").pack(pady=5)
new_location_entry = tk.Entry(scrollable_frame, width=40)
new_location_entry.pack(pady=5)
tk.Button(scrollable_frame, text="Add Location", command=lambda: add_location()).pack(pady=5)

# Tombol tambahan
tk.Button(scrollable_frame, text="Complete Task", command=complete_task).pack(pady=5)
tk.Button(scrollable_frame, text="Motivational Boost", command=show_motivation).pack(pady=5)

# Tombol untuk mengontrol timer mundur
tk.Button(scrollable_frame, text="Start Timer", command=start_timer).pack(pady=5)
tk.Button(scrollable_frame, text="Stop Timer", command=stop_timer).pack(pady=5)

# Pengaturan waktu istirahat
tk.Label(scrollable_frame, text="Set Break Time (minutes):").pack(pady=5)
break_time_entry = tk.Entry(scrollable_frame, width=20)
break_time_entry.pack(pady=5)
tk.Button(scrollable_frame, text="Set Break Time", command=set_break_time).pack(pady=5)

# Analisis waktu tidak produktif
tk.Button(scrollable_frame, text="Analyze Non-Productive Time", command=analyze_non_productive_time).pack(pady=5)

# Start Break Reminder Thread
break_thread = threading.Thread(target=remind_break, daemon=True)
break_thread.start()

# Run App
root.mainloop()
