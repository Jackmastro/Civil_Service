# TO INSTALL on RPi: 
#   - AM2320 library https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor/python-circuitpython
#   - TCA9548A library https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A
#   - SCD30 library https://github.com/adafruit/Adafruit_CircuitPython_SCD30

import board
import adafruit_ahtx0
import adafruit_tca9548a
import adafruit_scd30
import time
                         
# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the TCA9548A (multiplexer) object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

for channel in range (8):
    if tca[channel].try_lock():
        print("Channel {}:".format(channel), end="")
        addresses = tca[channel].scan()
        print([hex(address) for address in addresses if address!=0x70])
        tca[channel].unlock()

# Define AM2315C sensors connected to channels of the multiplexer
CO2_in = adafruit_scd30.SCD30(tca[0])
CO2_out = adafruit_scd30.SCD30(tca[1])
TrH_out = adafruit_ahtx0.AHTx0(tca[2])
TrH_in = adafruit_ahtx0.AHTx0(tca[3])
TrH_amb = adafruit_ahtx0.AHTx0(tca[4])
TrH_cool = adafruit_ahtx0.AHTx0(tca[5])


try: 
    while True:
        print(TrH_amb.temperature, TrH_amb.relative_humidity)
        print(TrH_cool.temperature, TrH_cool.relative_humidity)
        print(TrH_in.temperature, TrH_in.relative_humidity)
        print(TrH_out.temperature, TrH_out.relative_humidity)
#         print(CO2_in.CO2, TrH_out.temperature, TrH_in.temperature, TrH_amb.temperature, TrH_cool.temperature)
#         print(CO2_out.CO2, TrH_out.relative_humidity, TrH_in.relative_humidity, TrH_amb.relative_humidity, TrH_cool.relative_humidity)

        time.sleep(5.0)

except KeyboardInterrupt:
    
    print("You have successfully terminated the programm.")