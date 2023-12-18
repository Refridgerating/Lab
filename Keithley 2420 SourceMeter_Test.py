import pyvisa

def test_keithley_connection(gpib_address):
    rm = pyvisa.ResourceManager()
    keithley = rm.open_resource(gpib_address)
    print(f"Connected to: {keithley.query('*IDN?')}")

    # Perform a basic measurement (adjust the command according to your Keithley model)
    print(f"Voltage Measurement: {keithley.query(':MEAS:VOLT?')}")

    keithley.close()

test_keithley_connection('GPIB0::25::INSTR')  # Replace with your GPIB address
