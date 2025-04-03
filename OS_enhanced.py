import tkinter as tk
from tkinter import ttk
import psutil
import time
from threading import Thread

class SystemTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Resource Tracker")
        self.root.geometry("450x600")
        self.root.configure(bg="#2E3B4E")

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TProgressbar", thickness=20, troughcolor="#374A5A", background="#4CAF50")
        self.style.configure("green.Horizontal.TProgressbar", background="#4CAF50")
        self.style.configure("yellow.Horizontal.TProgressbar", background="#FFC107")
        self.style.configure("red.Horizontal.TProgressbar", background="#F44336")

        # Title Label
        self.header_label = tk.Label(root, text="System Resource Tracker", font=("Helvetica", 16, "bold"), bg="#2E3B4E", fg="white")
        self.header_label.pack(pady=10)

        # Memory Info
        self.memory_frame = tk.Frame(root, bg="#2E3B4E")
        self.memory_frame.pack(pady=10)
        self.memory_label = tk.Label(self.memory_frame, text="Total Memory Usage", font=("Helvetica", 14), bg="#2E3B4E", fg="white")
        self.memory_label.pack()
        self.memory_progress = ttk.Progressbar(self.memory_frame, orient="horizontal", length=300, mode="determinate", maximum=100)
        self.memory_progress.pack(pady=5)
        self.memory_info = tk.Label(self.memory_frame, text="--% Used", font=("Helvetica", 12), bg="#2E3B4E", fg="white")
        self.memory_info.pack()

        # Automatically detect available drives (excluding F:)
        all_partitions = psutil.disk_partitions()
        self.disks = [p.device for p in all_partitions if "F:\\" not in p.device]  # Excludes "F:\"
        self.disk_widgets = {}

        for disk in self.disks:
            self.create_disk_frame(disk)

        # Stop Button
        self.stop_button = tk.Button(root, text="Stop Tracking", command=self.stop_tracking, font=("Helvetica", 12, "bold"), bg="#D32F2F", fg="white", padx=10, pady=5, relief="flat")
        self.stop_button.pack(pady=20)

        self.tracking = True
        self.update_thread = Thread(target=self.update_system_stats, daemon=True)
        self.update_thread.start()

    def create_disk_frame(self, disk):
        """Create UI components for each available disk"""
        frame = tk.Frame(self.root, bg="#2E3B4E")
        frame.pack(pady=10)

        disk_label = tk.Label(frame, text=f"Disk {disk}", font=("Helvetica", 14), bg="#2E3B4E", fg="white")
        disk_label.pack()

        progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate", maximum=100)
        progress.pack(pady=5)

        info_label = tk.Label(frame, text="--% Used", font=("Helvetica", 12), bg="#2E3B4E", fg="white")
        info_label.pack()

        self.disk_widgets[disk] = (progress, info_label)

    def update_system_stats(self):
        """Continuously update memory and disk usage every second"""
        while self.tracking:
            # Update Memory Usage
            memory_info = psutil.virtual_memory()
            memory_percent = memory_info.percent
            self.root.after(0, self.update_memory, memory_percent)

            # Update each available disk
            for disk in self.disks:
                try:
                    disk_info = psutil.disk_usage(disk)
                    disk_percent = disk_info.percent
                    self.root.after(0, self.update_disk, disk, disk_percent)
                except Exception as e:
                    print(f"Error accessing {disk}: {e}")

            time.sleep(1)

    def update_memory(self, memory_percent):
        """Update total memory (RAM) usage dynamically"""
        self.memory_info.config(text=f"{memory_percent}% Used")
        self.memory_progress["value"] = memory_percent

        if memory_percent < 50:
            self.memory_progress.config(style="green.Horizontal.TProgressbar")
        elif memory_percent < 80:
            self.memory_progress.config(style="yellow.Horizontal.TProgressbar")
        else:
            self.memory_progress.config(style="red.Horizontal.TProgressbar")

    def update_disk(self, disk, disk_percent):
        """Update disk progress bars dynamically"""
        progress, info_label = self.disk_widgets[disk]
        info_label.config(text=f"{disk_percent}% Used")
        progress["value"] = disk_percent

        # Apply color coding
        if disk_percent < 50:
            progress.config(style="green.Horizontal.TProgressbar")
        elif disk_percent < 80:
            progress.config(style="yellow.Horizontal.TProgressbar")
        else:
            progress.config(style="red.Horizontal.TProgressbar")

    def stop_tracking(self):
        """Stop tracking and close the app"""
        self.tracking = False
        self.root.quit()

def run():
    root = tk.Tk()
    app = SystemTrackerApp(root)
    root.mainloop()
    return "System Resource Tracker app is running!"

if __name__ == "__main__":
    print(run())