import nidaqmx
import time
import csv
import pyvisa

class NIUSB6001:
    def __init__(self, ao_channel):
        self.ao_channel = ao_channel
        self.ao_task = None

    def initialize(self):
        self.ao_task = nidaqmx.Task()
        self.ao_task.ao_channels.add_ao_voltage_chan(self.ao_channel)

    def write_voltage(self, voltage):
        if self.ao_task:
            self.ao_task.write(voltage)

    def close(self):
        if self.ao_task:
            self.ao_task.close()

class Keithley2420:
    def __init__(self, address):
        self.address = address
        self.instrument = None

    def initialize(self):
        rm = pyvisa.ResourceManager()
        self.instrument = rm.open_resource(self.address)

    def read_voltage(self):
        return self.instrument.query(":MEAS:VOLT?")

    def close(self):
        if self.instrument:
            self.instrument.close()

def voltage_sweep_test(daq, keithley, file_path, start_voltage, end_voltage, num_steps):
    step_size = (end_voltage - start_voltage) / num_steps

    with open(file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['DAQ Voltage', 'Measured Voltage'])

        for i in range(num_steps + 1):
            voltage = start_voltage + i * step_size
            daq.write_voltage(voltage)

            raw_voltage = keithley.read_voltage()
            float_voltage = float(raw_voltage)
            print(f"Step {i}: DAQ Voltage = {voltage}, Measured Voltage = {float_voltage}")

            csv_writer.writerow([voltage, float_voltage])
            time.sleep(0.5)  # Adjust the delay as needed

def main():
    daq = NIUSB6001("Dev1/ao1")  # Replace with your actual AO channel
    keithley = Keithley2420('GPIB0::25::INSTR')  # Replace with your GPIB address

    try:
        daq.initialize()
        keithley.initialize()

        voltage_sweep_test(daq, keithley, "voltage_measurements.csv", 0, 5, 50)
    finally:
        daq.close()
        keithley.close()

if __name__ == "__main__":
    main()
