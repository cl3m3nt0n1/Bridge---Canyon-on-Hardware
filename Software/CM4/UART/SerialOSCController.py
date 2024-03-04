"""
SerialOSCController - Serial to OSC Communication Controller

Authors : @Cl3m3nt0n1 - @RomainH27
Licence : GPL3

This class reads data from a serial port, smoothens it, and sends OSC messages
to sushi based on the read addresses and values.
Any received message must be written like so : @address/integer_converted_value_of_a_pot


Attributes:
    - serial_port (str): The serial port from which to read data (default: '/dev/ttyS0').
    - osc_ip (str): The IP address of the OSC server to which to send messages (default: '127.0.0.1').
    - osc_port (int): The port of the OSC server to which to send messages (default: 24024).
    - smoothing_factor (float): The smoothing factor to smooth the read values (default: 0.2).
    - max_smoothed_values (int): The maximum number of smoothed values to retain (default: 10).
    - debug (bool): Enable debug mode to display additional information (default: False).

Methods:
    - __init__(self, serial_port, osc_ip, osc_port, smoothing_factor=0.2, max_smoothed_values=10, debug=False):
        Initializes a new instance of SerialOSCController.

    - process_serial_data(self):
        Reads data from the serial port, smoothes it, and sends OSC messages based on the read addresses and values.

    - is_variation_sufficient(self, address, smoothed_value):
        Checks if the variation between the new smoothed value and the previous one is significant enough to emit an OSC message.

    - route_osc_message(self, address, value):
        Routes OSC messages based on the read address.

    - send_osc_message(self, address, value):
        Sends an OSC message to the specified address with the specified value.

    - run(self):
        Executes the main loop to continuously read and process serial data.

"""
import RPi.GPIO as GPIO
from pythonosc import udp_client
import serial
import time

class SerialOSCController:
    def __init__(self, serial_port, osc_ip, osc_port, smoothing_factor=0.2, max_smoothed_values=10, debug=False):
        self.ser = serial.Serial(serial_port, 115200, timeout=1)
        self.ser.reset_input_buffer()
        self.osc_client = udp_client.SimpleUDPClient(osc_ip, osc_port)
        self.smoothing_factor = smoothing_factor
        self.max_smoothed_values = max_smoothed_values
        self.smoothed_values = {}
        self.debug = debug


    def send_osc_message(self, address, value):
        self.osc_client.send_message(address, value)


    def process_serial_data(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            address, raw_value = line.split('/')
            raw_value = int(raw_value)

            if address not in self.smoothed_values:
                self.smoothed_values[address] = [raw_value]
            else:
                # Adds a new value to list
                self.smoothed_values[address].append(raw_value)

                # Smoothing the incoming value
                smoothed_value = sum(self.smoothed_values[address]) / len(self.smoothed_values[address])

                # Going Low on RAM here
                self.smoothed_values[address] = self.smoothed_values[address][-self.max_smoothed_values:]

                if self.is_variation_sufficient(address, smoothed_value):
                    value = round(smoothed_value / 1024, 2)
                    self.route_osc_message(address, value)
                    if self.debug:
                        print("message sent : ", address, value) # DBG Only


    def is_variation_sufficient(self, address, smoothed_value):
        threshold = 1.2
        
        # Adds any previously unseen value
        if address not in self.smoothed_values or len(self.smoothed_values[address]) < 2:
            return True

        # Comparison with previous value
        previous_smoothed_value = self.smoothed_values[address][-2]
        variation = abs(smoothed_value - previous_smoothed_value)

        return variation > threshold


    def route_osc_message(self, address, value):
        if address == '@1':
            self.send_osc_message("/parameter/Canyon/Dry_Wet", value)
        elif address == '@2':
            self.send_osc_message("/parameter/Canyon/Gain", value)
        elif address == '@3':
            self.send_osc_message("/parameter/Canyon/Blend", value)
        elif address == '@4':
            self.send_osc_message("/parameter/Canyon/HighCut_Freq", value)
        elif address == '@5':
            self.send_osc_message("/parameter/Canyon/HighCut_FreqB", value)
        elif address == '@6':
            self.send_osc_message("/parameter/Canyon/LowCut_Freq", value)

    def negociate(self, serial_port):
        # Is arduino ready ?
        self.ser.write(b"READY?\n")
        self.ser.flush()
        time.sleep(1)

        # Hope it answers in less than 5 seconds
        start_time = time.time()
        timeout =  5  # Timeout in seconds
        while time.time() - start_time < timeout:
            if serial_port.in_waiting >  0:
                response = self.ser.readline().decode('utf-8').rstrip()
                print(response)
                if response == "OK":
                    return  # it's ready so, let's go
                else:
                    raise Exception("Unexpected response from the other device.")
            time.sleep(0.1)

        # Timeout reached, no answers...
        raise Exception("Negotiation timed out. The other device did not respond.")


    def run(self):
        self.negociate(self.ser)
        while True:
            self.process_serial_data()
