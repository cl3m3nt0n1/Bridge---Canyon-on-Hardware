import serial

class SerialPortManager:
    def __init__(self, default_ports=['/dev/ttyS0', '/dev/ttyAMA0'], baudrate=115200):
        self.default_ports = default_ports
        self.baudrate = baudrate

    def check_port_availability(self, port_name):
        try:
            serial_port = serial.Serial(port=port_name, baudrate=self.baudrate, timeout=1)
            serial_port.close()
            return True
        except serial.SerialException as err:
            return False

    def find_available_port(self, user_selected_port):
        if self.check_port_availability(user_selected_port):
            return user_selected_port
        else:
            for port in self.default_ports:
                if self.check_port_availability(port):
                    return port
            raise Exception("No available serial port found.")


