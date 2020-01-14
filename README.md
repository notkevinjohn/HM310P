# HM310P
## Python Modbus Implementation to control a HanmaTek HM310P DC Power Supply

I found a very cheap USB programmable DC Power Supply on Amazon. The price was great, but the software support was non-existent. I created the included python class to control this device using the minimalmodus library. This was a very quick and dirty implementation, but it got the job done. 

<img src="https://images-na.ssl-images-amazon.com/images/I/61FTSm9KMFL._SL1200_.jpg" alt="image" width="400"/>

I did not implement the full set of features for this device, just the ability to turn it on and off and set the voltage. The code that I wrote is for Linux and expects there to be a device at /dev/dcpowersupply. I have also included the udev rules file that will create the needed symlink for this device. 

You can examine or run the included example script. This will turn on the supply, and then step the voltage slowly up to 12V before turning off the supply. 

### Notes
The MODBUS implementation is not perfect. It often fails to communicate with the device. I solved this by having the code try until it succeeds. This is obviously not very effcient, but it suits my needs. 
