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


#### COLOUR PLOTS https://gist.github.com/justinmklam/090d92011c6b7c9510f86b4cb667be92
import time,board
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt

print("Initializing MLX90640")
i2c = board.I2C() # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate
mlx_shape = (24,32)
print("Initialized")

# setup the figure for plotting
plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
t_array = []
print("Starting loop")
while True:
    t1 = time.monotonic()
    try:
        mlx.getFrame(frame) # read MLX temperatures into frame var
        data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
        therm1.set_data(np.fliplr(data_array)) # flip left to right
        therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
        cbar.update_normal(therm1) # update colorbar range
        plt.title(f"Max Temp: {np.max(data_array):.1f}C")
        plt.pause(0.001) # required
        #fig.savefig('mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC', bbox_inches='tight') # comment out to speed up
        t_array.append(time.monotonic()-t1)
        print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
    except ValueError:
        continue # if error, just read again