import tkinter as tk
from tkinter import ttk
import psutil
import time
from threading import Thread

def run():
    """Function to run the System Resource Tracker app with enhanced UI."""
    root = tk.Tk()
    app = SystemTrackerApp(root)

    # Define styles for progress bars
    style = ttk.Style()
    style.theme_use("clam")  # Use modern theme
    style.configure("green.Horizontal.TProgressbar", thickness=20, background="green")
    style.configure("yellow.Horizontal.TProgressbar", thickness=20, background="yellow")
    style.configure("red.Horizontal.TProgressbar", thickness=20, background="red")

    root.mainloop()

class SystemTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Resource Tracker")
        self.root.geometry("450x500")
        self.root.configure(bg="#2E3B4E")  # Dark mode background
        
        # Header Label
        self.header_label = tk.Label(
            root, text="🔍 Real-Time System Resource Tracker", 
            font=("Helvetica", 16, "bold"), fg="#EAECEE", bg="#2E3B4E"
        )
        self.header_label.pack(pady=10)

        # Memory Frame
        self.memory_frame = tk.Frame(root, bg="#2E3B4E")
        self.memory_frame.pack(pady=10)

        # Memory Labels
        self.total_memory_label = self.create_label(self.memory_frame, "Total Memory: -- GB")
        self.used_memory_label = self.create_label(self.memory_frame, "Used Memory: -- GB")
        self.available_memory_label = self.create_label(self.memory_frame, "Available Memory: -- GB")
        self.memory_usage_label = self.create_label(self.memory_frame, "Memory Usage: --%")
        
        # Memory Progress Bar
        self.memory_progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", maximum=100)
        self.memory_progress.pack(pady=5)

        # Disk Frame
        self.disk_frame = tk.Frame(root, bg="#2E3B4E")
        self.disk_frame.pack(pady=10)

        # Disk Labels
        self.disk_usage_label = self.create_label(self.disk_frame, "Disk Usage: -- GB used")

        # Disk Progress Bar
        self.disk_progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", maximum=100)
        self.disk_progress.pack(pady=5)

        # Stop Button
        self.stop_button = tk.Button(
            root, text="⏹ Stop Tracking", command=self.stop_tracking, 
            font=("Helvetica", 12, "bold"), fg="white", bg="#E74C3C", 
            relief="flat", padx=10, pady=5, activebackground="#C0392B"
        )
        self.stop_button.pack(pady=20)

        self.tracking = True
        self.update_thread = Thread(target=self.update_system_stats, daemon=True)
        self.update_thread.start()

    def create_label(self, parent, text):
        """Creates a styled label."""
        label = tk.Label(parent, text=text, font=("Helvetica", 12), fg="#EAECEE", bg="#2E3B4E")
        label.pack(pady=3)
        return label

    def update_system_stats(self):
        while self.tracking:
            memory_info = psutil.virtual_memory()
            total_memory = memory_info.total / (1024 ** 3)
            used_memory = memory_info.used / (1024 ** 3)
            available_memory = memory_info.available / (1024 ** 3)
            memory_percent = memory_info.percent

            disk_info = psutil.disk_usage('C:/')
            disk_used = disk_info.used / (1024 ** 3)
            disk_percent = disk_info.percent

            self.root.after(0, self.update_memory_labels, total_memory, used_memory, available_memory, memory_percent)
            self.root.after(0, self.update_disk_labels, disk_used, disk_percent)

            time.sleep(1)

    def update_memory_labels(self, total_memory, used_memory, available_memory, memory_percent):
        self.total_memory_label.config(text=f"Total Memory: {total_memory:.2f} GB")
        self.used_memory_label.config(text=f"Used Memory: {used_memory:.2f} GB")
        self.available_memory_label.config(text=f"Available Memory: {available_memory:.2f} GB")
        self.memory_usage_label.config(text=f"Memory Usage: {memory_percent}%")

        self.memory_progress['value'] = memory_percent
        self.set_progressbar_style(self.memory_progress, memory_percent)

    def update_disk_labels(self, disk_used, disk_percent):
        self.disk_usage_label.config(text=f"Disk Usage: {disk_used:.2f} GB used")
        self.disk_progress['value'] = disk_percent
        self.set_progressbar_style(self.disk_progress, disk_percent)

    def set_progressbar_style(self, progress_bar, percent):
        if percent < 50:
            progress_bar.config(style="green.Horizontal.TProgressbar")
        elif percent < 80:
            progress_bar.config(style="yellow.Horizontal.TProgressbar")
        else:
            progress_bar.config(style="red.Horizontal.TProgressbar")

    def stop_tracking(self):
        self.tracking = False
        self.root.quit()

if __name__ == "__main__":
    run()