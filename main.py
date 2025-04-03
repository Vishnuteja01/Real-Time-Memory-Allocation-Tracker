import tkinter as tk
from tkinter import ttk
import OS_multiple
import OS_enhanced
import Paging

class IntegratedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Simulation Tool")
        self.root.geometry("600x400")
        self.root.configure(bg="#1E1E1E")  # Greyish Black Background

        # Apply Greyish Black Theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12), padding=6, background="#3A3A3A", foreground="white")
        style.map("TButton", background=[("active", "#555555")])  # Lighter Grey on Hover
        style.configure("TLabel", background="#1E1E1E", foreground="#D3D3D3", font=("Helvetica", 12))

        # Title Label
        self.title_label = tk.Label(
            root, text="OS Real Time Memory Management Tool",
            font=("Helvetica", 16, "bold"), bg="#1E1E1E", fg="#E0E0E0"  # Light Grey Title
        )
        self.title_label.pack(pady=10)

        # Buttons
        self.disk_button = ttk.Button(root, text="Run OS RAM", command=self.run_os_multiple_disks)
        self.disk_button.pack(pady=5)

        self.enhanced_button = ttk.Button(root, text="Run OS ROM", command=self.run_os_enhanced)
        self.enhanced_button.pack(pady=5)

        self.paging_button = ttk.Button(root, text="Run Paging and Segmentation", command=self.run_paging)
        self.paging_button.pack(pady=5)

        # Output Label
        self.output_label = tk.Label(
            root, text="Output will appear here", font=("Helvetica", 12),
            bg="#2E2E2E", fg="white", padx=10, pady=5, anchor="center", wraplength=500
        )
        self.output_label.pack(pady=20, fill="x", expand=True)

    def run_os_multiple_disks(self):
        result = OS_multiple.run()
        self.output_label.config(text=result)

    def run_os_enhanced(self):
        result = OS_enhanced.run()
        self.output_label.config(text=result)

    def run_paging(self):
        result = Paging.run()
        self.output_label.config(text=result)

if __name__ == "__main__":
    root = tk.Tk()
    app = IntegratedGUI(root)
    root.mainloop()