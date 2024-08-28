import minimalmodbus
import serial
import pandas as pd
import time

class MightyZap():
    def __init__(self, port='COM4', address=1, initialize=False):
        """
        Initializes the MightyZap class.

        :param port: The serial port to connect to (default 'COM3').
        :param address: The Modbus address of the device (default 1).
        :param initialize: If True, initializes the device settings upon creation.
        """
        self.port = port
        self.address = address
        self.open()
        if initialize: 
            self.initialize()
    
    def open(self):
        """
        Establishes a connection to the MightyZap device using the Modbus protocol.
        Configures the serial communication settings, including baud rate, bytesize, parity, stopbits, and timeout.
        """
        # Initialize the Modbus instrument with the specified port and address
        self.inst = minimalmodbus.Instrument(self.port, self.address)

        # Set serial communication parameters
        self.inst.serial.baudrate = 57600        # Baud rate: 19200
        self.inst.serial.bytesize = 8            # Data bits: 8
        self.inst.serial.parity   = serial.PARITY_NONE  # No parity
        self.inst.serial.stopbits = 1            # Stop bits: 1
        self.inst.serial.timeout  = 10            # Timeout: 1 second

        # Set the communication mode to ASCII
        self.inst.mode = minimalmodbus.MODE_ASCII 

        # Clear the buffers before each transaction to ensure clean communication
        self.inst.clear_buffers_before_each_transaction = True

    def read_register(self, register, signed=False):
        """
        Reads data from a specified Modbus register.

        :param register: The register address to read from (e.g., 30001 for input register).
        :param signed: True if the data should be interpreted as signed integer.
        :return: The data read from the register.
        """
        if register > 40000:
            # Adjust for holding register address range (40xxx)
            data = self.inst.read_register(registeraddress=register-40001, functioncode=3, signed=signed)
        elif register < 40000:
            # Adjust for input register address range (30xxx)
            data = self.inst.read_register(registeraddress=register-30001, functioncode=4, signed=signed)
        return data

    def close(self):
        """Close the serial connection."""
        if self.serial.is_open:
            self.serial.close()

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.close()