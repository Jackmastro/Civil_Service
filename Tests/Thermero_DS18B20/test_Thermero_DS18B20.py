#  pip install w1thermsensor
#  https://pypi.org/project/w1thermsensor/

from w1thermsensor import W1ThermSensor, Sensor
import RPi.GPIO as GPIO
import time
import os

# Set GPIO mode to Board numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO pin number
gpio_Tlarvero_pin = 4

# Set GPIO pin as output
GPIO.setup(gpio_Tlarvero_pin, GPIO.IN)

# device_folders = os.listdir('/sys/bus/w1/devices/')
# sensor_addresses = [folder for folder in device_folders if folder.startswith('28-')]
# for folder in sensor_addresses:
#     print('Sensor address:', folder)
# print(sensor_addresses)

sensorList = []
loop = 1

try:
    while True:
        count = 1
        for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
            print(count, "  ID: %s     T: %.2f" % (sensor.id, sensor.get_temperature()))
            
            if loop == 1:
                sensorList.append(sensor.id)
            count += 1
        
        loop += 1
    
except KeyboardInterrupt:
    print("You have successfully terminated the programm.")
    print(sensorList)
    
finally:
    GPIO.cleanup()