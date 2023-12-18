import numpy as np
import time
import csv
import os

def sweep_magnetic_field(ni_usb6001, keithley, file_path, start_voltage, end_voltage, num_steps, sweep_time):
    step_time = sweep_time / num_steps

    with open(file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        # Write the header
        csv_writer.writerow(['Step Voltage', 'Measured Voltage', 'float voltage', 'Current', 'Resistance'])

        # Function to perform a single sweep
        def single_sweep(direction):
            for step in np.linspace(start_voltage, end_voltage, num_steps)[::direction]:
                ni_usb6001.write_voltage(step)
                voltage = keithley.instrument.query(":MEAS:VOLT?")
                current = keithley.instrument.query(":MEAS:CURR?")
                resistance = keithley.instrument.query(":MEAS:RES?")
                response = keithley.instrument.query(":MEAS:VOLT?").strip()
                measurements = response.split(',')
                voltage_measurement = float(measurements[0])
                csv_writer.writerow([step, voltage, voltage_measurement, current, resistance])
                time.sleep(step_time)

        # Forward sweep
        single_sweep(1)
        # Reverse sweep
        single_sweep(-1)

        # Reset the output voltage to 0 at the end of the sweep
        ni_usb6001.write_voltage(0)