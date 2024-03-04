#!/usr/bin/env python3
from UART.SerialOSCController import SerialOSCController
from UART.SerialPortManager import SerialPortManager
import subprocess, sys
import argparse, os

# Refuse to launch if user is not sudo
if os.geteuid() != 0:
    print("You need to be a superuser to run this program.")
    exit(1)

# Parsing args
parser = argparse.ArgumentParser(description='SerialOSCController')
parser.add_argument('--serial_port', type=str, default='/dev/ttyS0', help='Serial port')
parser.add_argument('--osc_ip', type=str, default='127.0.0.1', help='OSC IP address')
parser.add_argument('--osc_port', type=int, default=24024, help='OSC port')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')

args = parser.parse_args()

# if the specified port is unavailable, try the other one and use it if it works.
portManager = SerialPortManager()
args.serial_port = portManager.find_available_port(args.serial_port)

# Prevent an input/output error crash due to tty usage on specified port
command = "systemctl stop serial-getty@" + args.serial_port.split("/")[2] + ".service"
subprocess.run(command, shell = True, executable="/bin/bash")

controller = SerialOSCController(
    serial_port=args.serial_port,
    osc_ip=args.osc_ip,
    osc_port=args.osc_port,
    debug=args.debug
)

print(f"SerialOSCController started successfully on port {args.serial_port}. Debug mode {'is' if args.debug else 'is not'} enabled.")


# Main loop
controller.run()
