# TO INSTALL on RPi: 
#   - AM2320 library https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor/python-circuitpython
#   - TCA9548A library https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A

import board
import adafruit_ahtx0
import adafruit_tca9548a
import time
from gpiozero import OutputDevice

# Set fan
Suct_fans = OutputDevice(23, active_high=False)
Suct_fans.on()
             
# Create I2C bus as normal
i2c = board.I2C()

# Create the TCA9548A (multiplexer) object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# Define AM2315C sensors connected to channels of the multiplexer
TrH_out = adafruit_ahtx0.AHTx0(tca[2])
TrH_in = adafruit_ahtx0.AHTx0(tca[3])
TrH_amb = adafruit_ahtx0.AHTx0(tca[4])
TrH_cool = adafruit_ahtx0.AHTx0(tca[5])

try: 
    while True:
        print(TrH_out.temperature, TrH_in.temperature, TrH_amb.temperature, TrH_cool.temperature)
        print(TrH_out.relative_humidity, TrH_in.relative_humidity, TrH_amb.relative_humidity, TrH_cool.relative_humidity)

        time.sleep(3.0)

except KeyboardInterrupt:
    print("You have successfully interrupted the programm.")

finally:
    Suct_fans.off()
    Suct_fans.close()
    print("You have successfully cleaned the pins.")