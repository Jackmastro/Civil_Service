# TO INSTALL on RPi: 
#   - AM2320 library https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor/python-circuitpython
#   - TCA9548A library https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A
#   - board
#   - busio
#   - csv
#
import board
# import busio
# import adafruit_am2320
# import adafruit_tca9548a

import time
import sys
# import os

# import csv
# import traceback
# import board #Python module that abstracts away the underlying hardware and provides a high-level API(Application Programming Interface) for accessing and controlling devices connected to the Raspberry Pi's GPIO pins, I2C buses, SPI buses, and other interfaces.
# import busio #Python module that provides a unified API for working with various bus protocols, such as I2C and SPI. It allows you to create I2C and SPI bus objects that you can use to communicate with devices.
# from Multiplexer_TCA9548A import adafruit_tca9548a
# import TrH_AM2315.AM2315
# import TrH_AM2315.adasmbus
# import AM2315

# # # # # # # # # # # # # # # # # # # # #  FUNZIONA 
sys.path.append('/TrH_AM2315')
print("ok")


from TrH_AM2315 import AM2315
print("ok")
from TrH_AM2315 import adasmbus
print("ok")

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

TrH_try = AM2315.AM2315(i2c)
# # # # # # # # # # # # # # # # # # # # # # # # # # #                      

                            


# # Create the TCA9548A (multiplexer) object and give it the I2C bus
# tca = adafruit_tca9548a.TCA9548A(i2c)

# for channel in range (8):
#     if tca[channel].try_lock():
#         print("Channel {}:".format(channel), end="")
#         addresses = tca[channel].scan()
#         print([hex(address) for address in addresses if address!=0x70])
#         tca[channel].unlock()

# # Define AM2315 sensors connected to channels of the multiplexer
# TrH_out = AM2315.AM2315(mux[2])
# TrH_in = AM2315.AM2315(mux[3])
# TrH_amb = AM2315.AM2315(mux[4]) # if "import adafruit_am2315" then adafruit_am2320.AM2320(..)
# TrH_try = adafruit_am2320.AM2320(i2c)




# Create list to store and paste sensor values in a csv file 
# data = []

try: 
    while True:
        # Read humidity and t emperature vales from sensors. It returns a tuple, an unchangeable list of values.
#         TrH_out = TrH_out.read_humidity_temperature() 
#         TrH_in = TrH_in.read_humidity_temperature()
#         TrH_amb = TrH_amb.read_humidity_temperature()
# 
#         print("Outlet: H,T ", TrH_out)
#         print("Inlet: H,T ", TrH_in)
#         print("Ambient: H,T ", TrH_amb)
        print("ok")
        T = TrH_try.read_temperature()
        print(T)
#         rH = TrH_try.read_humidity()
#         print(rH)
#         print("Temperature:", )
#         print("Humidity:", TrH_try.relative_humidity)

#         data.append({'sensor_id': 'T&rH out', 'temperature': TrH_out[1], 'humidity': TrH_out[0], 'time': time.time},
#                     {'sensor_id': 'T&rH in', 'temperature': TrH_in[1], 'humidity': TrH_in[0], 'time': time.time},
#                     {'sensor_id': 'T&rH amb', 'temperature': TrH_amb[1], 'humidity': TrH_amb[0], 'time': time.time})

        time.sleep(1.0)

except KeyboardInterrupt:
#     print("\nKeyboard Interrupt: Saving data in a csv file")
# 
#     # Define the fieldnames for the CSV file
#     fieldnames = ['sensor_id', 'temperature', 'humidity', 'time']
# 
#     # Write the data to a CSV file
#     with open('sensor_data.csv', mode='w') as csv_file:
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)

    print("You have successfully terminated the programm.")