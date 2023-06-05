# pip install hx711
# pip3 install 'git+https://github.com/gandalf15/HX711.git#egg=HX711&subdirectory=HX711_Python3'

import RPi.GPIO as GPIO
import hx711
import time

# Set GPIO mode to Board numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO pin numbers
gpio_kgScale_pin = 16#36
clk_kgScale_pin = 5#29

# Set GPIO pin as output&input
GPIO.setup(gpio_kgScale_pin, GPIO.IN)
GPIO.setup(clk_kgScale_pin, GPIO.OUT)
gain = 64
channel = 'A'
# Define HX711 load cell sensor
LoadCell = hx711.HX711(dout_pin=gpio_kgScale_pin, # Rpi input
              pd_sck_pin=clk_kgScale_pin, # RPi output
              gain_channel_A=gain, # The higher the gain, the more sensitive the load cell readings will be, but the more noisy the signal may become (Alternative: 32, 64 & 128).
              select_channel=channel) # Either A or B

# Set ratio for current channel
ratio = 44.678 # Value taken from calibration
LoadCell.set_scale_ratio(ratio)

# Set offset
# LoadCell.zero()
# offset = LoadCell.get_current_offset()
# print(offset)
# LoadCell.set_offset(offset, channel=channel, gain_A=gain)
offset = 98127 # Value taken from calibration
LoadCell.set_offset(offset, channel=channel, gain_A=gain)

try:
    while True:
        weight = LoadCell.get_weight_mean(readings=20)
        print(f"The weight is: {round(weight, 2)} g")
        time.sleep(0.5)
    
except KeyboardInterrupt:
    print("You have successfully terminated the programm.")

finally: # The finally block in Python is always executed, regardless of whether an exception was raised or not. 
    GPIO.cleanup()