# # github.com/Sensirion/python-i2c-sfm-sf06/blob/master/sensirion_i2c_sfm_sf06
# import argparse
# import time
# import RPi.GPIO as GPIO
# from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
# from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
# from sensirion_i2c_sfm_sf06.device import SfmSf06Device
# from gpiozero import OutputDevice # More suitable for fans, motors and pumps instead of LED
# 
# # Set suction fan
# Suct_fans = OutputDevice(19, active_high=False)
# Suct_fans.on()
# 
# # Set mass flow sensor
# parser = argparse.ArgumentParser()
# parser.add_argument('--i2c_port', '-p', default='/dev/i2c-1')
# args = parser.parse_args()
# 
# with LinuxI2cTransceiver(args.i2c_port) as i2c_transceiver:
#     channel = I2cChannel(I2cConnection(i2c_transceiver),
#                          slave_address=0x29,
#                          crc=CrcCalculator(8, 0x31, 0xff, 0x0))
#     sensor = SfmSf06Device(channel)
# #     try:
# #         sensor.stop_continuous_measurement()
# #         time.sleep(1)
# #     except BaseException:
# #         ...
# #     (product_identifier, serial_number
# #      ) = sensor.read_product_identifier()
# #     print(f"product_identifier: {product_identifier}; "
# #           f"serial_number: {serial_number}; "
# #           )
#     sensor.stop_continuous_measurement()
#     sensor.start_air_continuous_measurement()
#     try:
#         for i in range(100):
#             time.sleep(1)
#             (a_flow, a_temperature, a_status_word
#              ) = sensor.read_measurement_data()
# #             print(f"a_flow: {a_flow}; "
# #                   f"a_temperatur---e: {a_temperature}; "
# #                   f"a_status_word: {a_status_word}; "
# #                   )
#             print(a_flow)
#         Suct_fans.off()
#         Suct_fans.close()
#         sensor.stop_continuous_measurement()
#         print("Loop terminated")
#         
#     except KeyboardInterrupt: 
#         Suct_fans.off()
#         Suct_fans.close()
#         sensor.stop_continuous_measurement()
#         print("Loop interrupted")


# github.com/Sensirion/python-i2c-sfm-sf06/blob/master/sensirion_i2c_sfm_sf06
import argparse
import time
import numpy as np
import RPi.GPIO as GPIO
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_sfm_sf06.device import SfmSf06Device
from gpiozero import OutputDevice # More suitable for fans, motors and pumps instead of LED

# Set suction fan
Suct_fans = OutputDevice(19, active_high=False)
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
    for i in range(100):
        time.sleep(1)
        (air_flow, air_temperature, _) = sensor.read_measurement_data()
        print(f"Air flow: {air_flow} L/min \n"
              f"Air flow: {air_flow.value * conversion / area} m/s \n"
              f"Air temperature: {air_temperature}° \n"
              )
    Suct_fans.off()
    Suct_fans.close()
    sensor.stop_continuous_measurement()
    print("Loop terminated")
    
except KeyboardInterrupt: 
    Suct_fans.off()
    Suct_fans.close()
    sensor.stop_continuous_measurement()
    print("Loop interrupted")
