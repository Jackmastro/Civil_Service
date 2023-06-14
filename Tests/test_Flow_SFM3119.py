# Flow SFM3119 library https://sensirion.github.io/python-i2c-sfm-sf06/ (https://github.com/Sensirion/python-i2c-sfm-sf06/blob/master/sensirion_i2c_sfm_sf06)
# sudo i2cdetect -y 1 (0x29)
import argparse
import time
import numpy as np
# https://pypi.org/project/sensirion-i2c-driver/
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
# https://pypi.org/project/sensirion-driver-adapters/
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_sfm_sf06.device import SfmSf06Device
from gpiozero import OutputDevice

# Set suction fan
Suct_fans = OutputDevice(23, active_high=False)
Suct_fans.on()

# Set mass flow sensor
parser = argparse.ArgumentParser()
parser.add_argument('--i2c_port', '-p', default='/dev/i2c-1')
args = parser.parse_args()

i2c_transceiver = LinuxI2cTransceiver(args.i2c_port)
i2c_transceiver.open()

channel = I2cChannel(I2cConnection(i2c_transceiver),
                     slave_address=0x29,
                     crc=CrcCalculator(8, 0x31, 0xff, 0x0))
sensor = SfmSf06Device(channel)

sensor.stop_continuous_measurement()
sensor.start_air_continuous_measurement()

area = (0.0166 / 2)**2 * np.pi
conversion = 1 / 16670
try:
    while True:
        time.sleep(5.0)
        (air_flow, air_temperature, _) = sensor.read_measurement_data()
        print(f"Air flow: {air_flow} L/min \n"
              f"Air flow: {air_flow.value * conversion / area} m/s \n"
              f"Air temperature: {air_temperature}° \n"
              )
    
except KeyboardInterrupt:
    print("You have successfully interrupted the programm.")

finally:
    Suct_fans.off()
    Suct_fans.close()
    sensor.stop_continuous_measurement()
    print("You have successfully cleaned the pins.")