# Analog-to-Digital Converter MCP3008 library https://https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx
from NH3_MQ137 import MQ137
import busio
import time
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as mcp3008
# from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select, enable disable communication)
cs = digitalio.DigitalInOut(board.D8)

# create the mcp object
mcp = mcp3008.MCP3008(spi, cs)

# create NH3 sensor object
NH3_out = MQ137.MQ137(mcp, Ro=141, analogPin=0)
NH3_in = MQ137.MQ137(mcp, Ro=141, analogPin=1)

try: 
    while True:
        print(NH3_out.MQGetGasPercentage())
        print(NH3_in.MQGetGasPercentage())

except KeyboardInterrupt:
    print("You have successfully interrupted the programm.")