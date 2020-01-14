#!/usr/bin/python3
from HM310P import HM310P
import time

supply = HM310P()
supply.set_voltage(0)
supply.power_on()
time.sleep(5)  
for i in range(0,101):
    supply.set_voltage(i/100*12)
    time.sleep(3)
supply.power_off()