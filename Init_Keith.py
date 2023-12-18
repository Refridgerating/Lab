import pyvisa

class Keithley2420:
    def __init__(self, address):
        self.address = address
        self.instrument = None

    def initialize(self):
        rm = pyvisa.ResourceManager()
        self.instrument = rm.open_resource(self.address)
        self.instrument.write('*RST')
        self.instrument.write(':SOUR:FUNC CURR')
        self.instrument.write(':SENS:FUNC "VOLT"')
        print(f"Keithley 2420 at {self.address} initialized.")

    def close(self):
        if self.instrument:
            self.instrument.close()
            print(f"Keithley 2420 at {self.address} closed.")
