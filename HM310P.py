#!/usr/bin/python3

import minimalmodbus
import serial
import time


class HM310P():

    rDepth = 100

    def __init__(self):
        self.supply = minimalmodbus.Instrument('/dev/dcpowersupply', 1, minimalmodbus.MODE_RTU)
        self.supply.serial.baudrate = 9600
        self.supply.serial.startbits = 1
        self.supply.serial.stopbits = 1
        self.supply.serial.parity = serial.PARITY_NONE
        self.supply.serial.bytesize = 8
        self.supply.timeout = 0.5

##########################
#### Power Management ####
##########################

    def get_power(self):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.read_power()
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def read_power(self):
        try:
            power = self.supply.read_register(1, 0)
            return power
        except:
            return "Error"

    def power_on(self):
        self.set_power(1)

    def power_off(self):
        self.set_power(0)

    def set_power(self, status):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.write_power(status)
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def write_power(self, status):
        try:
            self.supply.write_register(1, status, 0)
            return True
        except:
            return "Error"

############################
#### Voltage Management ####
############################

    def get_voltage(self):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.read_voltage()
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def read_voltage(self):
        try:
            voltage = self.supply.read_register(16, 2)
            return voltage
        except:
            return "Error"

    def get_set_voltage(self):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.read_set_voltage()
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def read_set_voltage(self):
        try:
            voltage = self.supply.read_register(48, 2)
            return voltage
        except:
            return "Error"

    def set_voltage(self, voltage):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.write_voltage(voltage)
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def write_voltage(self, voltage):
        try:
            self.supply.write_register(48, voltage, 2)
            return True
        except:
            return "Error"
    
############################
#### Current Management ####
############################

    def get_current(self):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.read_voltage()
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def read_current(self):
        try:
            voltage = self.supply.read_register(17, 2)
            return voltage
        except:
            return "Error"

    def get_set_current(self):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.read_set_current()
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def read_set_current(self):
        try:
            voltage = self.supply.read_register(49, 2)
            return voltage
        except:
            return "Error"

    def set_current(self, current):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.write_current(current)
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def write_current(self, current):
        try:
            self.supply.write_register(49, current, 2)
            return True
        except:
            return "Error"

###############################
#### Protection Management ####
###############################

    def get_set_overvoltageprotection(self):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.read_set_overvoltageprotection()
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def read_set_overvoltageprotection(self):
        try:
            voltage = self.supply.read_register(32, 2)
            return voltage
        except:
            return "Error"

    def get_set_overcurrentprotection(self):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.read_set_overcurrentprotection()
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def read_set_overcurrentprotection(self):
        try:
            voltage = self.supply.read_register(33, 2)
            return voltage
        except:
            return "Error"
    
    def set_overvoltageprotection(self, voltage):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.write_overvoltageprotection(voltage)
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def write_overvoltageprotection(self, voltage):
        try:
            self.supply.write_register(32, voltage, 2)
            return True
        except:
            return "Error"

    def set_overcurrentprotection(self, current):
        r = 0
        value = "Error"
        while r <= self.rDepth:
            value = self.write_overcurrentprotection(current * 10)
            if not value == "Error":
                return value
            r += 1
            time.sleep(0.001)
        return False

    def write_overcurrentprotection(self, current):
        try:
            self.supply.write_register(33, current, 2)
            return True
        except:
            return "Error"


if __name__ == "__main__":
    supply = HM310P()
    supply.set_voltage(0)
    supply.power_on()
    time.sleep(5)  
    for i in range(0, 101):
        supply.set_voltage(i/100*5)
        time.sleep(3)
        
    supply.power_off()

