#!/usr/bin/python3

import minimalmodbus
import serial
import time


class HM310P():
    rDepth = 100

    def __init__(self):
        self.supply = minimalmodbus.Instrument('COM4', 1, minimalmodbus.MODE_RTU)
        self.supply.serial.baudrate = 9600
        self.supply.serial.startbits = 1
        self.supply.serial.stopbits = 1
        self.supply.serial.parity = serial.PARITY_NONE
        self.supply.serial.bytesize = 8
        self.supply.timeout = 0.5
        # functions using template
        self.get_power = self.__rtu_template(self.get_power)
        self.set_power = self.__rtu_template(self.set_power)
        self.get_voltage = self.__rtu_template(self.get_voltage)
        self.get_set_voltage = self.__rtu_template(self.get_set_voltage)
        self.set_voltage = self.__rtu_template(self.set_voltage)
        self.get_current = self.__rtu_template(self.get_current)
        self.get_set_current = self.__rtu_template(self.get_set_current)
        self.set_current = self.__rtu_template(self.set_current)
        self.get_set_overvoltageprotection = self.__rtu_template(self.get_set_overvoltageprotection)
        self.get_set_overcurrentprotection = self.__rtu_template(self.get_set_overcurrentprotection)
        self.set_overvoltageprotection = self.__rtu_template(self.set_overvoltageprotection)
        self.set_overcurrentprotection = self.__rtu_template(self.set_overcurrentprotection)

    # wrapper
    def __rtu_template(self, func):
        def wrapper(*argv):
            r = 0
            value = "Error"
            while r <= self.rDepth:
                try:
                    value = func(*argv)
                    return value
                except:
                    r += 1
                    time.sleep(0.001)
            return False
        return wrapper

    ##########################
    #### Power Management ####
    ##########################

    def get_power(self, *argv):
        return self.supply.read_register(1, 0)

    def power_on(self, *argv):
        self.set_power(1)

    def power_off(self, *argv):
        self.set_power(0)

    def set_power(self, status):
        return self.supply.write_register(1, status, 0)

    ############################
    #### Voltage Management ####
    ############################

    def get_voltage(self, *argv):
        return self.supply.read_register(16, 2)

    def get_set_voltage(self, *argv):
        return self.supply.read_register(48, 2)

    def set_voltage(self, voltage):
        return self.supply.write_register(48, voltage, 2)

    ############################
    #### Current Management ####
    ############################

    def get_current(self, *argv):
        return self.supply.read_register(17, 2)

    def get_set_current(self, *argv):
        return self.supply.read_register(49, 2)

    def set_current(self, current):
        return self.supply.write_register(49, current, 2)

    ###############################
    #### Protection Management ####
    ###############################

    def get_set_overvoltageprotection(self, *argv):
        return self.supply.read_register(32, 2)

    def get_set_overcurrentprotection(self, *argv):
        return self.supply.read_register(33, 2)

    def set_overvoltageprotection(self, voltage):
        return self.supply.write_register(32, voltage, 2)

    def set_overcurrentprotection(self, current):
        return self.supply.write_register(33, current, 2)


if __name__ == "__main__":
    supply = HM310P()
    print(supply.get_power())
    supply.power_on()
    print(supply.get_power())
    time.sleep(5)
    supply.power_off()
