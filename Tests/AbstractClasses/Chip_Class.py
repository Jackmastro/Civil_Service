# General imports
from abc import ABC, abstractmethod
import board

# Multiplexer TCA9548A library https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A
import adafruit_tca9548a
# Analog-to-Digital Converter MCP3008 library https://https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx
import digitalio
import adafruit_mcp3xxx.mcp3008 as mcp3008
from adafruit_mcp3xxx.analog_in import AnalogIn as analog_in

class Chip(ABC):
    def __init__(self, name):
        self.name = name
        self.chip = None

    @abstractmethod
    def set_channel(self, sensor_name):
        pass

class Multiplexer_TCA9548A(Chip):
    def __init__(self, name):
        super().__init__(name)
        
        # Create I2C bus as normal
        i2c = board.I2C()

        # Create the Multiplexer TCA9548A object and give the I2C bus to it
        self.chip = adafruit_tca9548a.TCA9548A(i2c)

        print(f"Setup for {self.name} successfully completed.")

    def set_channel(self, sensor_name):
        if 'CO2' in sensor_name and 'out' in sensor_name:
            return self.chip[0]
        elif 'CO2' in sensor_name and 'in' in sensor_name:
            return self.chip[1]
        elif 'TrH' in sensor_name and 'out' in sensor_name:
            return self.chip[2]
        elif 'TrH' in sensor_name and 'in' in sensor_name:
            return self.chip[3]
        elif 'TrH' in sensor_name and 'amb' in sensor_name:
            return self.chip[4]
        elif 'TrH' in sensor_name and 'cool' in sensor_name:
            return self.chip[5]
        elif 'extra2' in sensor_name:
            return self.chip[6]
        elif 'extra3' in sensor_name:
            return self.chip[7]
        else:
            raise ValueError('sensor_name has to be "CO2", "TrH", "extra2" or "extra3" + "in", "out", "amb" or "cool". Received: {}'.format(sensor_name))

    def test(self):
        for channel in range (8):
            if self.chip[channel].try_lock():
                print("Channel {}:".format(channel), end="")
                addresses = self.chip[channel].scan()
                print([hex(address) for address in addresses if address!=0x70])
                self.chip[channel].unlock()

class ADC_MCP3008(Chip):
    def __init__(self, name):
        super().__init__(name)

        self.channel = []

        # Create the SPI bus
        spi = board.SPI()

        # Create the CS (chip select, enable disable communication)
        cs = digitalio.DigitalInOut(board.D8)

        # Create the Analog-to-Digital Converter MCP3008 object and give the SPI bus and CS to it
        self.chip = mcp3008.MCP3008(spi, cs)

        print(f"Setup for {self.name} successfully completed.")

    def set_channel(self, sensor_name):
        if 'NH3' in sensor_name and 'out' in sensor_name:
            self.channel = analog_in(self.chip, mcp3008.P0)
            return self.channel
        elif 'NH3' in sensor_name and 'in' in sensor_name:
            self.channel = analog_in(self.chip, mcp3008.P1)
            return self.channel
        elif 'extra1' in sensor_name:
            self.channel = analog_in(self.chip, mcp3008.P2)
            return self.channel
        elif 'extra2' in sensor_name:
            self.channel = analog_in(self.chip, mcp3008.P3)
            return self.channel
        elif 'extra3' in sensor_name:
            self.channel = analog_in(self.chip, mcp3008.P4)
            return self.channel
        else:
            raise ValueError('sensor_name has to be "NH3", "TrH", "extra1", "extra2" or "extra3" + "in" or "out". Received: {}'.format(sensor_name))