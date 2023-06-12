#  pip install ds18b20
#  https://github.com/rgbkrk/ds18b20

from ds18b20 import DS18B20
import RPi.GPIO as GPIO
import time

# Set GPIO mode to Board numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO pin number
gpio_Tlarvero_pin = 4

# Set GPIO pin as output
GPIO.setup(gpio_Tlarvero_pin, GPIO.IN)

sensors = []
sensors = DS18B20.get_all_sensors()
print(sensors)
for sensor_id in DS18B20.get_available_sensors():
    sensors.append(DS18B20(sensor_id))
print(sensors)

Tbefore= time.time()
for sensor in sensors:
    print("Sensor %s has temperature %.2f" % (sensor.get_id(), sensor.get_temperature()))
Tafter = time.time()
print("time taken {}".format(Tafter-Tbefore))