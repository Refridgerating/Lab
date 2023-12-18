import tkinter as tk
from tkinter import filedialog
from Init_Keith import Keithley2420
from Init_DAQ import NIUSB6001
from magnetic_field_control import sweep_magnetic_field
import threading

class MagneticFieldApp:
    def __init__(self, master):
        self.master = master
        master.title("Magnetic Field Control")

        # Entry fields
        self.start_voltage = tk.DoubleVar()
        self.end_voltage = tk.DoubleVar()
        self.num_steps = tk.IntVar()
        self.sweep_time = tk.DoubleVar()

        tk.Label(master, text="Start Voltage:").grid(row=0)
        tk.Entry(master, textvariable=self.start_voltage).grid(row=0, column=1)

        tk.Label(master, text="End Voltage:").grid(row=1)
        tk.Entry(master, textvariable=self.end_voltage).grid(row=1, column=1)

        tk.Label(master, text="Number of Steps:").grid(row=2)
        tk.Entry(master, textvariable=self.num_steps).grid(row=2, column=1)

        tk.Label(master, text="Sweep Time:").grid(row=3)
        tk.Entry(master, textvariable=self.sweep_time).grid(row=3, column=1)

        # Start button
        self.start_button = tk.Button(master, text="Start Sweep", command=self.start_sweep)
        self.start_button.grid(row=4, columnspan=2)

        # File save path
        self.file_path = tk.StringVar()
        tk.Label(master, text="Save Path:").grid(row=5)
        tk.Entry(master, textvariable=self.file_path).grid(row=5, column=1)
        tk.Button(master, text="Browse", command=self.browse_file).grid(row=5, column=2)

    def browse_file(self):
        self.file_path.set(filedialog.asksaveasfilename(defaultextension=".csv"))

    def start_sweep(self):
        # Thread the sweep so it doesn't block the main thread
        threading.Thread(target=self.run_sweep, daemon=True).start()

    def run_sweep(self):
        # Instantiate the Keithley 2420
        keithley = Keithley2420('GPIB0::25::INSTR')
        keithley.initialize()

        # Instantiate the NI USB 6001 DAQ with the analog output channel
        ni_usb6001 = NIUSB6001("Dev1/ao1")  # Replace with your actual AO channel
        ni_usb6001.initialize()

        # Corrected indentation starts here
        sweep_magnetic_field(ni_usb6001, keithley, self.file_path.get(), 
                            self.start_voltage.get(), self.end_voltage.get(),
                            self.num_steps.get(), self.sweep_time.get())

        keithley.close()
        ni_usb6001.close()

def main():
    root = tk.Tk()
    app = MagneticFieldApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
