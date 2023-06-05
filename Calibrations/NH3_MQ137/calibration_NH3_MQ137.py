from MQ137 import MQ137
import busio
import time
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as mcp3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select, enable disable communication)
cs = digitalio.DigitalInOut(board.D8)

# create the mcp object
mcp = mcp3008.MCP3008(spi, cs)

# create NH3 sensor object
NH3_out = MQ137(mcp, analogPin=0)
NH3_in = MQ137(mcp, analogPin=1)

try: 
    while True:
        print("Ro = ", NH3_out.MQCalibration())
        print("Ro = ", NH3_in.MQCalibration())

except KeyboardInterrupt:
    print("You have successfully terminated the programm. \n Remember to insert the Ro value in the sensor constructor that you find in the class sensor and test scrpits.")