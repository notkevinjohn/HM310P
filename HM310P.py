#!/usr/bin/python3

import minimalmodbus
import serial
import time


class HM310P:

    def __init__(self, t_port='/dev/dcpowersupply', t_address=1):
        self.supply = minimalmodbus.Instrument(t_port, t_address, minimalmodbus.MODE_RTU)
        self.supply.serial.baudrate = 9600
        self.supply.serial.startbits = 1
        self.supply.serial.stopbits = 1
        self.supply.serial.parity = serial.PARITY_NONE
        self.supply.serial.bytesize = 8
        self.supply.timeout = 0.5
        self.rDepth = 50
        # functions using template
        self.get_data = self.__rtu_template(self.get_data)
        self.set_data = self.__rtu_template(self.set_data)

    # wrapper
    def __rtu_template(self, func):
        def wrapper(*argv):
            r = 0
            while r <= self.rDepth:
                try:
                    value = func(*argv)
                    return value
                except IOError:
                    r += 1
                    time.sleep(0.001)
            return False
        return wrapper

    # read function
    def get_data(self, *argv):
        return self.supply.read_register(*argv)

    # set function
    def set_data(self, *argv):
        return self.supply.write_register(*argv)

    # sets functions to global (some don't work(only red))
    def _do_global(self, func, *argv):
        copy_address = self.supply.address
        self.supply.address = 0
        copy = self.rDepth
        self.rDepth = 10
        value = func(*argv)
        self.rDepth = copy
        self.supply.address = copy_address
        return value

    ##########################
    #### Power Management ####
    ##########################

    def get_power(self):
        return self.get_data(1, 0)

    def power_on(self):
        self.set_power(1)

    def global_power_on(self):
        self.set_global_power(1)

    def power_off(self):
        self.set_power(0)

    def global_power_off(self):
        self.set_global_power(0)

    def set_power(self, status):
        self.set_data(1, status, 0)

    def set_global_power(self, status):
        self._do_global(self.set_power, status)

    ############################
    #### Voltage Management ####
    ############################

    def get_voltage(self):
        return self.get_data(16, 2)

    def get_set_voltage(self):
        return self.get_data(48, 2)

    def set_voltage(self, voltage):
        self.set_data(48, voltage, 2)

    ############################
    #### Current Management ####
    ############################

    def get_current(self):
        return self.get_data(17, 3)

    def get_set_current(self):
        return self.get_data(49, 3)

    def set_current(self, current):
        self.set_data(49, current, 3)

    #########################
    #### Watt Management ####
    #########################

    def get_watt(self):
        return ((self.get_data(0x12, 0) << 16) + self.get_data(0x13, 0)) * 0.001

    ###############################
    #### Protection Management ####
    ###############################

    def get_set_overvoltageprotection(self):
        return self.get_data(32, 2)

    def get_set_overcurrentprotection(self):
        return self.get_data(33, 3)

    def set_overvoltageprotection(self, voltage):
        self.set_data(32, voltage, 2)

    def set_overcurrentprotection(self, current):
        self.set_data(33, current, 3)

    def set_overpowerprotection(self, watt):
        watt = int(watt * 10)
        self.set_data(0x22, (watt & 0xffff0000) >> 16, 0)
        self.set_data(0x23, watt & 0x0000ffff, 0)

    def get_set_overpowerprotection(self):
        return ((self.get_data(0x22, 0) << 16) + self.get_data(0x23, 0)) * 0.01

    def get_protection_on(self):
        return self.get_data(0x02, 0)

    def get_overvoltageprotection(self):
        return self.get_protection_on() & 0b0001

    def get_overcurrentprotection(self):
        return self.get_protection_on() & 0b0010

    def get_overpowerprotection(self):
        return self.get_protection_on() & 0b0010

    def get_overtemperaturprotection(self):
        return self.get_protection_on() & 0b0100

    def get_shortcircuitprotection(self):
        return self.get_protection_on() & 0b1000

    # communication Waning: do only if you know what you doing.
    def set_communicationaddress(self, address):
        self.set_data(0x9999, address, 0)

    def get_set_communicationaddress(self):
        return self.get_data(0x9999, 0)

    # Power supply specification (first half V, second half A)
    def get_specification(self):
        return self.get_data(0x3, 0)

    def get_tailclassification(self):
        return self.get_data(0x4, 0)

    def get_decimalpointdigitcopacity(self):
        return self.get_data(0x5, 0)

    # master config
    def master_get_slave_addres(self):
        return self.supply.address

    def master_set_slave_addres(self, t_address):
        self.supply.address = t_address


if __name__ == "__main__":
    supply = HM310P()
    supply.power_on()
    print("current client address: " + str(supply.get_set_communicationaddress()))  # prints current address
    supply.set_communicationaddress(2)  # you power supply form address 1 is now address 2
    supply.master_set_slave_addres(2)  # sets master to talk to address 2
    supply.power_off()
    time.sleep(2)
    print("resetting changes")
    supply.set_communicationaddress(1)  # sets power supply form address 2 to address 1
    supply.master_set_slave_addres(1)  # resets master to address 1
