import tkinter as tk
from tkinter import ttk, messagebox
import psutil

class ProcessMemoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Process Memory Usage")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#2E3B4E")  # Dark mode background

        # Style for widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=6, background="#34495E", foreground="white")
        self.style.map("TButton", background=[("active", "#555555")])
        self.style.configure("TLabel", font=("Helvetica", 12), padding=5, background="#EAECEE", foreground="#EAECEE")

        # Title Label
        self.title_label = tk.Label(root, text="🔍 Real-Time Process Memory Visualization",
                                    font=("Helvetica", 16, "bold"), bg="#2E3B4E", fg="#EAECEE")
        self.title_label.pack(pady=10)

        # Progress Bar for Total Memory Usage
        self.memory_frame = tk.Frame(root, bg="#2E3B4E")
        self.memory_frame.pack(pady=10, fill=tk.X)

        self.memory_usage_label = tk.Label(self.memory_frame, text="Total Memory Usage", font=("Helvetica", 12), bg="#2E3B4E", fg="white")
        self.memory_usage_label.pack(pady=5)
        self.memory_progress = ttk.Progressbar(self.memory_frame, orient="horizontal", length=400, mode="determinate", maximum=100)
        self.memory_progress.pack()

        # Scrollable Canvas for Process Memory Visualization
        self.canvas_frame = tk.Frame(root, bg="#2E3B4E")
        self.canvas_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.process_canvas = tk.Canvas(self.canvas_frame, width=800, height=400, bg="#34495E", bd=2, relief="solid")
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.process_canvas.yview)
        self.process_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = tk.Frame(self.process_canvas, bg="#34495E")
        self.process_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.process_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scroll_frame.bind("<Configure>", lambda e: self.process_canvas.configure(scrollregion=self.process_canvas.bbox("all")))

        # Control Buttons
        self.control_frame = tk.Frame(root, bg="#2E3B4E")
        self.control_frame.pack(pady=10)

        self.start_button = ttk.Button(self.control_frame, text="▶ Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=20)

        self.stop_button = ttk.Button(self.control_frame, text="⏹ Stop", command=self.stop_tracking, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=20)

        self.tracking = False

    def start_simulation(self):
        if not self.tracking:
            self.tracking = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.update_process_stats()

    def update_process_stats(self):
        if self.tracking:
            try:
                memory_info = psutil.virtual_memory()
                memory_percent = memory_info.percent
                self.memory_progress["value"] = memory_percent
                self.visualize_processes()
            except Exception as e:
                print(f"Error: {e}")
            self.root.after(5000, self.update_process_stats)

    def visualize_processes(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        processes = list(psutil.process_iter(['pid', 'name', 'memory_info']))[:15]
        for process in processes:
            try:
                name = process.info['name']
                memory_usage = process.info['memory_info'].rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

            if memory_usage == 0:
                continue

            process_frame = tk.Frame(self.scroll_frame, pady=5, bg="#34495E")
            process_frame.pack(fill="x", padx=10)

            self.visualize_paging(process_frame, name, memory_usage)
            self.visualize_segmentation(process_frame, name, memory_usage)

            process_label = tk.Label(process_frame, text=f"{name} ({memory_usage:.2f} MB)", font=("Helvetica", 12, "bold"), bg="#34495E", fg="white")
            process_label.pack(pady=5)

    def visualize_paging(self, parent, name, memory_usage):
        page_size = 10
        total_pages = max(1, int(memory_usage / page_size))
        paging_frame = tk.Frame(parent, bg="#1ABC9C")
        paging_frame.pack(side="left", padx=20)
        for i in range(total_pages):
            page_label = tk.Label(paging_frame, text=f"Page {i+1}", bg="#16A085", relief="solid", padx=5, pady=3)
            page_label.pack(side="left", padx=2)

    def visualize_segmentation(self, parent, name, memory_usage):
        segment_sizes = [int(memory_usage * 0.3), int(memory_usage * 0.4), int(memory_usage * 0.2), int(memory_usage * 0.1)]
        segment_names = ["Code", "Data", "Stack", "Heap"]
        segmentation_frame = tk.Frame(parent, bg="#F39C12")
        segmentation_frame.pack(side="left", padx=20)
        for segment_name, segment_size in zip(segment_names, segment_sizes):
            segment_label = tk.Label(segmentation_frame, text=f"{segment_name}\n{segment_size}MB", bg="#D35400", relief="solid", padx=10, pady=5)
            segment_label.pack(side="left", padx=2)

    def stop_tracking(self):
        self.tracking = False
        messagebox.showinfo("Simulation Stopped", "The process memory tracking has been stopped.")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def run(self):
        self.root.mainloop()

# ✅ Function to run the app when imported
def run():
    root = tk.Tk()
    app = ProcessMemoryApp(root)
    app.run()

# ✅ If run directly, start the app
if __name__ == "__main__":
    run()