import nidaqmx
import time

def test_daq_output(ao_channel):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(ao_channel)
        print(f"Setting voltage on {ao_channel}.")

        # Set a test voltage, e.g., 2.5V
        Voltage = 10
        task.write(Voltage)
        print(f"Setting voltage to {Voltage}.")
        time.sleep(2)  # Wait for x seconds

        # Reset the voltage to 0V
        task.write(0)
        print(f"Voltage reset on {ao_channel}.")

test_daq_output("Dev1/ao1") 
