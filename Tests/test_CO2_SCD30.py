import time
import board
import adafruit_scd30
import adafruit_tca9548a
from gpiozero import OutputDevice 
import RPi.GPIO as GPIO

# Set suction fan
Suct_fans = OutputDevice(19, active_high=False)
Suct_fans.on()


# Create I2C bus as normal. Datasheet recommends starting at 50KHz
i2c = board.I2C()  # uses board.SCL and board.SDA
# Create the TCA9548A (multiplexer) object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)
# Define CO2 sensors
CO2_in = adafruit_scd30.SCD30(tca[0])
CO2_out = adafruit_scd30.SCD30(tca[1])

try: 
    while True:
        # since the measurement interval is long (2+ seconds) we check for new data before reading
        # the values, to ensure current readings.
        if CO2_in.data_available:
            print("Inlet:", CO2_in.CO2, "PPM", CO2_in.temperature, "°C", CO2_in.relative_humidity, "%")
            print("Outlet:", CO2_out.CO2, "PPM", CO2_out.temperature, "°C", CO2_out.relative_humidity, "%")

        time.sleep(5.0)
        
except KeyboardInterrupt:
    print("You have successfully interrupted the programm.")
finally:
    Suct_fans.off()
    Suct_fans.close()
#     GPIO.cleanup()
    print("You have successfully cleaned the pins.")
    
    
    
    
        