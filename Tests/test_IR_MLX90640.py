# IR MLX90640 library https://github.com/adafruit/Adafruit_CircuitPython_MLX90640
# sudo pip3 install matplotlib scipy numpy
# sudo apt-get install -y python-smbus
# sudo apt-get install -y i2c-tools
# sudo i2cdetect -y 1 (0x33)

# sudo pip3 install RPI.GPIO adafruit-blinka
# sudo pip3 install adafruit-circuitpython-mlx90640

import time
import board
import numpy as np
import adafruit_mlx90640
import RPi.GPIO as GPIO
# import matplotlib.pyplot as plt

# Set-up I2C bus
i2c = board.I2C()

# Define MLX90640 IR camera on RPi
mlx = adafruit_mlx90640.MLX90640(i2c)

# Set-up refresh rate. The camera captures data at a rates defined in RefreshRate class (available: 0_5,1,2,4,8,16,32,64).
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ 

# Set-up camera pixel size 
mlx_shape = (24,32)

# Set-up array for storing all 768 temperatures (24x32 pixels)
frame = np.zeros((mlx_shape[0]*mlx_shape[1],1))
    
try:
    while True:
        print("New")
        mlx.getFrame(frame)
        frame = np.round(frame, 2)
        print(np.reshape(frame,mlx_shape))
        time.sleep(5.0)
        
except KeyboardInterrupt:
    print("You have successfully terminated the programm.")
    
finally:
    GPIO.cleanup()