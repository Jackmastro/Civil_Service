# GENERAL IMPORT
import RPi.GPIO as GPIO
import datetime
import time

from LCD_Class import *
from Chip_Class import *
from Sensor_Class import *
from Actuator_Class import *
from Controller_Class import *
from Saver_Class import *

GPIO.setmode(GPIO.BCM)

Thermero = Thermero_DS18B20("Thermero")
RTClock = RTC_DS1307("RTClock")

Thermero.read_data()
Thermero.read_data_point()
RTClock.save_data()
Thermero.save_data()
Thermero.save_data_point()
saver.save_Thermero_data(RTClock, Thermero)