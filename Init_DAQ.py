import nidaqmx

class NIUSB6001:
    def __init__(self, ao_channel):
        self.ao_channel = ao_channel
        self.ao_task = None  # Define the analog output task

    def initialize(self):
        self.ao_task = nidaqmx.Task()
        self.ao_task.ao_channels.add_ao_voltage_chan(self.ao_channel)
        print(f"NI USB 6001 DAQ output channel {self.ao_channel} initialized.")

    def write_voltage(self, voltage):
        if self.ao_task:
            self.ao_task.write(voltage)

    def close(self):
        if self.ao_task:
            self.ao_task.close()
            print(f"NI USB 6001 DAQ output channel {self.ao_channel} closed.")

