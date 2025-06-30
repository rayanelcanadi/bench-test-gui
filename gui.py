
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class BenchTestGUI:
    def __init__(self, root, serial_reader):
        self.root = root
        self.root.title("Bench Test GUI")
        self.serial_reader = serial_reader

        # COM port selection
        self.com_label = ttk.Label(root, text="Select COM Port:")
        self.com_label.pack(pady=5)
        self.combobox = ttk.Combobox(root, values=self.serial_reader.list_serial_ports())
        self.combobox.pack(pady=5)

        self.connect_button = ttk.Button(root, text="Connect", command=self.connect_serial)
        self.connect_button.pack(pady=5)

        self.start_button = ttk.Button(root, text="Start", command=self.start_acquisition)
        self.start_button.pack(pady=5)
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_acquisition)
        self.stop_button.pack(pady=5)

        # Graph setup
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(6,8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ani = FuncAnimation(self.fig, self.update_plot, interval=100)

    def connect_serial(self):
        port = self.combobox.get()
        try:
            self.serial_reader.connect(port)
            messagebox.showinfo("Success", f"Connected to {port}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_acquisition(self):
        self.serial_reader.start()

    def stop_acquisition(self):
        self.serial_reader.stop()

    def update_plot(self, frame):
        data = self.serial_reader.get_data()
        if not data['time']:
            return

        self.ax1.clear()
        self.ax1.plot(data['time'], data['power_percent'])
        self.ax1.set_title("% Puissance envoyée vs Temps")

        self.ax2.clear()
        self.ax2.plot(data['time'], data['thrust'])
        self.ax2.set_title("Poussée vs Temps")

        self.ax3.clear()
        self.ax3.plot(data['electrical_power'], data['thrust'])
        self.ax3.set_title("Puissance électrique vs Poussée")

        self.fig.tight_layout()
        self.canvas.draw()
