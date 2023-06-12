# General imports
from abc import ABC, abstractmethod
import RPi.GPIO as GPIO
import numpy as np
import board
import time
import math

# Import the Chip abstract class
from Chip_Class import *
# Import the LCD class
from LCD_Class import *
# CO2 SCD30 library https://github.com/adafruit/Adafruit_CircuitPython_SCD30
import adafruit_scd30
# TrH AM2320 library https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor/python-circuitpython
import adafruit_ahtx0
# IR MLX90640 library https://github.com/adafruit/Adafruit_CircuitPython_MLX90640
import adafruit_mlx90640
# RTC Real Time Cloack DS1307 library https://docs.circuitpython.org/projects/ds1307/en/latest/index.html
import adafruit_ds1307
# Flow SFM3119 library https://github.com/Sensirion/python-i2c-sfm-sf06/blob/master/sensirion_i2c_sfm_sf06
import argparse
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_sfm_sf06.device import SfmSf06Device
# Thermero DS18B20 https://pypi.org/project/w1thermsensor/
from w1thermsensor import W1ThermSensor
from w1thermsensor import Sensor as SensorType
# Scale HX711 https://github.com/gandalf15/HX711.git#egg=HX711&subdirectory=HX711_Python3
import hx711
# NH3 MQ137 sensor: https://tutorials-raspberrypi.com/configure-and-read-out-the-raspberry-pi-gas-sensor-mq-x/

GPIO.setmode(GPIO.BCM)

class Sensor(ABC):
    def __init__(self, name=str) -> None:
        self.name = name
        self.unit = str
        self.data_table = []
        self.sensor = None

    @abstractmethod
    def read_data(self) -> float:
        pass

    @abstractmethod
    def read_data_point(self) -> float:
        pass

    @abstractmethod
    def save_data(self) -> None:
        pass

    @abstractmethod
    def save_data_point(self) -> None:
        pass

# I2C
class RTC_DS1307(Sensor):
    def __init__(self, name=str) -> None:
        super().__init__(name)

        self.unit = "time"

        # Set the RTC Real Time Clock with the i2c channel
        i2c = board.I2C()
        self.sensor = adafruit_ds1307.DS1307(i2c)
        
        print(f"Setup for {self.name} successfully completed.")
        
    def read_data(self):
        return self.read_data_point()
    
    def read_data_point(self):
        t = self.sensor.datetime
        data_point = '{}_{}_{}_{}_{}_{}'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        return data_point
    
    def save_data(self):
        self.data_table.append(self.read_data())
    
    def save_data_point(self):
        self.data_table.append(self.read_data_point())
        
class CO2_SCD30(Sensor):
    def __init__(self, name=str, tca=None) -> None:
        super().__init__(name)
        
        self.unit = "ppm"

        # Set the CO2 sensor through the multiplexer given its name
        self.sensor = adafruit_scd30.SCD30(tca.set_channel(self.name))

        print(f"Setup for {self.name} successfully completed.")

    def read_data(self):
        data = [self.sensor.CO2, self.sensor.temperature, self.sensor.relative_humidity]
        return np.round(data, 2)
    
    def read_data_point(self):
        return np.round(self.sensor.CO2, 2)
    
    def save_data(self):
        self.data_table.append(self.read_data_point()) # Interested in CO2 values
    
    def save_data_point(self):
        self.data_table.append(self.read_data_point())

class TrH_AM2315C(Sensor):
    def __init__(self, name=str, tca=None) -> None:
        super().__init__(name)
        
        self.unit = "°C and %"

        # Set the temperature and relative humidity sensor through the multiplexer given its name
        self.sensor = adafruit_ahtx0.AHTx0(tca.set_channel(self.name))

        print(f"Setup for {self.name} successfully completed.")
    
    def read_data(self):
        data = [self.sensor.temperature, self.sensor.relative_humidity]
        return np.round(data, 2)
    
    def read_data_point(self):
        return np.round(self.sensor.temperature, 2)

    def save_data(self):
        self.data_table.append(self.read_data())

    def save_data_point(self):
        self.data_table.append(self.read_data_point())

class IR_MLX90640(Sensor):
    def __init__(self, name=str) -> None:
        super().__init__(name)

        self.unit = "°C"

        # Setup camera pixel size 
        self.shape = (24, 32)

        # Set the IR camera with the i2c channel
        i2c = board.I2C()
        self.sensor = adafruit_mlx90640.MLX90640(i2c)

        # Setup refresh rate. The camera captures data at a rates defined in RefreshRate class (available: 0_5,1,2,4,8,16,32,64).
#         self.sensor.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
############################TODO CHECK IF WORKS ALSO WITHOUT
        print(f"Setup for {self.name} successfully completed.")

    def read_data(self):
        # Setup array for storing all 768 temperatures (24x32 pixels)
        frame = np.zeros((self.shape[0] * self.shape[1], 1))
        self.sensor.getFrame(frame)
        frame = np.ravel(frame) # Flatten to 1x768
        return np.round(frame, 2)
    
    def read_data_point(self):
        temperature_mean = np.mean(self.read_data())
        return np.round(temperature_mean, 2)
    
    def save_data(self):
        self.data_table.append(self.read_data())
    
    def save_data_point(self):
        self.data_table.append(self.read_data_point())

class Flow_SFM3119(Sensor):
    def __init__(self, name=str) -> None:
        super().__init__(name)

        self.unit = "L/min"
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--i2c_port', '-p', default='/dev/i2c-1')
        args = parser.parse_args()
        i2c_transceiver = LinuxI2cTransceiver(args.i2c_port)
        i2c_transceiver.open()
        channel = I2cChannel(I2cConnection(i2c_transceiver),
                            slave_address=0x29,
                            crc=CrcCalculator(8, 0x31, 0xff, 0x0))
        
        # Set the flow sensor with the i2c channel
        self.sensor = SfmSf06Device(channel)
        self.sensor.stop_continuous_measurement()

        print(f"Setup for {self.name} successfully completed.")
        
    def read_data(self, type="L/min"):
        self.sensor.start_air_continuous_measurement()
        time.sleep(1) # Needed to get data
        (air_flow, air_temperature, _) = self.sensor.read_measurement_data()
        self.sensor.stop_continuous_measurement()
        
        # Get value from pointers
        temperature_value = air_temperature.value
        flow_value_Lmin = air_flow.value

        # Filter only positive values
        if flow_value_Lmin < 0:
            flow_value_Lmin = 0
        
        if type == "L/min":
            data = [np.round(flow_value_Lmin, 2), np.round(temperature_value, 2)]
            return data
        
        elif type == "m/s":
            self.unit = type
            
            # Perform conversion from L/min to m/s
            area = (0.0166 / 2)**2 * np.pi # Taken from datasheet
            flow_value_ms = flow_value_Lmin / (area * 16670)
            data = [np.round(flow_value_ms, 2), np.round(temperature_value, 2)]
            return data
        else:
            raise ValueError('type has to be "L/min" or "m/s". Received: {}'.format(type))

    def read_data_point(self, type="L/min"):
        [flow_value, _] = self.read_data(type=type)
        return flow_value
    
    def save_data(self):
        self.data_table.append(self.read_data_point()) # Interested in flow values
    
    def save_data_point(self):
        self.data_table.append(self.read_data_point())

# SPI
class Scale_HX711(Sensor):
    def __init__(self, name=str) -> None:
        super().__init__(name)

        self.unit = "g"

        # Set values of the scale
        channel = 'A' # Either A or B
        gain = 64 # The higher the gain, the more sensitive the load cell readings will be, but the more noisy the signal may become (Alternative: 32, 64 & 128).
        ratio = 44.678 # Value taken from calibration
        offset = 98127 # Value taken from calibration

        # Set GPIO pin numbers
        gpio_Scale_BCM = 16 #36
        clk_Scale_BCM = 5 #29
        
        # Set GPIO pin as input and output
        GPIO.setup(gpio_Scale_BCM, GPIO.IN)
        GPIO.setup(clk_Scale_BCM, GPIO.OUT)

        # Set load cell through the HX711 Analog-to-Digital Converter
        self.sensor = hx711.HX711(dout_pin=gpio_Scale_BCM, # Rpi input
                               pd_sck_pin=clk_Scale_BCM, # RPi output
                               gain_channel_A=gain,
                               select_channel=channel)
        
        # Set ratio taken from calibration
        self.sensor.set_scale_ratio(ratio)

        # Set offset taken from calibration
        self.sensor.set_offset(offset=offset, channel=channel, gain_A=gain)
        
        print(f"Setup for {self.name} successfully completed.")
        
    def read_data(self):
        return self.read_data_point()
    
    def read_data_point(self):
        data_point = self.sensor.get_weight_mean(readings=20)
        return np.round(data_point, 2)
    
    def save_data(self):
        self.data_table.append(self.read_data_point()) # Interested in g values
    
    def save_data_point(self):
        self.data_table.append(self.read_data_point())

class NH3_MQ137(Sensor):
    def __init__(self, name=str, mcp=None) -> None:
        super().__init__(name)

        self.unit = "ppm"

        # Set the NH3 sensor through the Analog-to-Digital Converter given its name
        self.sensor = mcp.set_channel(self.name)

        print(f"Setup for {self.name} successfully completed.")
        
    def NH3(self) -> float:
        Rl = 5.6 # kOhm. Value taken from hat schematics
        Ro = 141 # Value taken from calibration
        ref_16bit = 65472.0 # 10 bit scale with 6 digit shift
        # Calculation taken from https://ioct.tech/edu/sites/default/files/2019-04/MQ-2%20Gas%20Sensor%20--%20Educational.pdf
        Rs = float(Rl * (ref_16bit - self.sensor.value) / float(self.sensor.value))

        # NH3 sensitivity curve parameters: log(y) = m * log(x) + q
        m = -0.0024
        q = math.log(0.582) - m * math.log(1)
        x = Rs / Ro
        return math.pow(10, ((math.log(x) - q) / m))
        
    def read_data(self):
        return self.read_data_point()
    
    def read_data_point(self):
        data_point = self.NH3()
        return np.round(data_point, 2)
    
    def save_data(self):
        self.data_table.append(self.read_data())
    
    def save_data_point(self):
        self.data_table.append(self.read_data_point())

# 1-Wire
class Thermero_DS18B20(Sensor):
    def __init__(self, name=str) -> None:
        super().__init__(name)

        self.unit = "°C"

        gpio_Thermero_BCM = 4 #7
        GPIO.setup(gpio_Thermero_BCM, GPIO.IN)

        # Sensor dictionary with address after 28- as key and Raspberry Pi ordered counter as value
        self.physical_order_dict = {
            "00000e743370": 12,  # A1
            "00000e74b77f": 3,   # A2
            "00000e74378f": 18,  # A3
            "00000e74c185": 7,   # A4
            "00000e72abdd": 11,  # A5
            "00000e74c839": 1,   # B1
            "00000e737902": 5,   # B2
            "00000e74c6ef": 4,   # B3
            "00000e72d1a9": 9,   # B4
            "00000e73f4ec": 2,   # B5
            "00000e72dbe9": 15,  # C1
            "00000e745a03": 16,  # C2
            "00000e74667f": 6,   # C3
            "00000e9ae94c": 13,  # C4 "00000e73e6af"
            "00000e737785": 19,  # C5
            "00000e73f830": 14,  # D1
            "00000e728757": 8,   # D2
            "00000e744177": 20,  # D3
            "00000e9ab2c3": 17,  # D4 "00000e73ef44"
            "00000e9b86f4": 10   # D5 "00000e72e2b9"
        }

        # Set all the 1-wire temperature sensors of the type of interest
        self.sensor = W1ThermSensor.get_available_sensors([SensorType.DS18B20])

        print(f"Setup for {self.name} successfully completed.")

    def read_data(self):
        data = [single_sensor.get_temperature() for single_sensor in self.sensor]
#         print(data)
# [25.0625, 24.8125, 23.875, 24.9375, 25.5, 25.1875, 24.875, 24.375, 24.125, 24.6875, 24.75, 23.9375, 25.75, 24.1875, 24.6875, 24.5625, 25.25, 24.5625, 25.6875, 25.375]
        data = np.ravel(data) # Flatten to 1x20
#         print(data)
# [25.125  24.8125 23.875  24.9375 25.5    25.1875 24.875  24.375  24.125
#  24.6875 24.75   24.     25.75   24.1875 24.6875 24.5    25.25   24.5625
#  25.6875 25.375 ]
        return np.round(data, 2)

    def read_data_point(self):
        temperature_mean = np.mean(self.read_data())
        return np.round(temperature_mean, 2)

    def save_data(self):
        # Populate order_data_vec using advanced indexing
        order_data_vec = np.zeros((1, 20))  # 20 sensors in total
        order_data_vec[0, [value - 1 for value in self.physical_order_dict.values()]] = self.read_data() # Python indexing: value reduced by 1
#         print(order_data_vec)
#         [[25.19 24.69 24.81 24.38 24.88 25.75 24.94 25.25 24.12 25.38 25.5  25.06
#   24.19 24.56 24.75 23.94 25.69 23.88 24.69 24.56]]
        self.data_table.append(order_data_vec)

    def save_data_point(self):
        self.data_table.append(self.read_data_point())

#####################################################################################
# tca = Multiplexer_TCA9548A("TCA")
# CO2in = CO2_SCD30("CO2in", tca)
# CO2out = CO2_SCD30("CO2out", tca)
# try:
#     while True:
#         dataIn = CO2in.read_data_point()
#         dataOut = CO2out.read_data_point()
#         print(dataIn, dataOut)
#         print("-----------------------------")
#         time.sleep(3)
# 
# tca = Multiplexer_TCA9548A("TCA")
# TrHin = TrH_AM2315C("TrHin", tca)
# TrHout = TrH_AM2315C("TrHout", tca)
# TrHamb = TrH_AM2315C("TrHamb", tca)
# TrHcool = TrH_AM2315C("TrHcool", tca)
# try:
#     while True:
#         dataIn = TrHin.read_data()
#         print(dataIn, "\n")
#         dataOut = TrHout.read_data()
#         print(dataOut, "\n")
#         dataAmb = TrHamb.read_data()
#         print(dataAmb, "\n")
#         dataCool = TrHcool.read_data()
#         print(dataCool, "\n")
#         print("-----------------------------")
#         time.sleep(3)
    
# IRcamera = IR_MLX90640("IRcamera")
# try:
#     while True:
#         IRcamera.save_data()
#         print(IRcamera.data_table)
#         print("-----------------------------")
#         time.sleep(3)
# 
# except KeyboardInterrupt:
#     print("You have successfully terminated the programm.")
    
# Flow = Flow_SFM3119("Flow")
# try:
#     while True:
#         data = Flow.read_data()
#         print(data)
#         print("-----------------------------")
#         time.sleep(3)

# Thermero = Thermero_DS18B20("Thermero")
# try:
#     while True:
#         data = Thermero.read_data()
#         print(data)
#         print("-----------------------------")
#         time.sleep(3)

# Scale = Scale_HX711("Scale")
# try:
#     while True:
#         data = Scale.read_data_point()
#         print(data)
#         print("-----------------------------")
#         time.sleep(3)

# mcp = ADC_MCP3008("MCP")
# NH3out = NH3_MQ137("NH3out", mcp)
# NH3in = NH3_MQ137("NH3in", mcp)
# try:
#     while True:
#         dataOut = NH3out.read_data_point()
#         print(dataOut)
#         dataIn = NH3in.read_data_point()
#         print(dataIn)
#         print("-----------------------------")
#         time.sleep(3)
#     
# except KeyboardInterrupt:
#     print("You have successfully terminated the programm.")
# 
# Thermero = Thermero_DS18B20("Thermero")
# try:
#     while True:
#         Thermero.save_data()
#         print(Thermero.data_table)
#         print("-----------------------------")
#         time.sleep(3)
#         
# except KeyboardInterrupt:
#     print("You have successfully terminated the programm.")

# RTClock = RTC_DS1307("RTClock")
# try:
#     while True:
#         data = RTClock.read_data()
#         print(data)
#         RTClock.save_data_point()
#         print(RTClock.data_table)
#         print("-----------------------------")
#         time.sleep(3)
#     
# except KeyboardInterrupt:
#     print("You have successfully terminated the programm.")

##################################################################
# TCA = Multiplexer_TCA9548A("TCA")
# CO2in = CO2_SCD30("CO2in", TCA)
# CO2out = CO2_SCD30("CO2out", TCA)
# TrHin = TrH_AM2315C("TrHin", TCA)
# TrHout = TrH_AM2315C("TrHout", TCA)
# TrHamb = TrH_AM2315C("TrHamb", TCA)
# TrHcool = TrH_AM2315C("TrHcool", TCA)
# IRcamera = IR_MLX90640("IRcamera")
# Flow = Flow_SFM3119("Flow")
# Scale = Scale_HX711("Scale")
# MCP = ADC_MCP3008("MCP")
# NH3out = NH3_MQ137("NH3out", MCP)
# NH3in = NH3_MQ137("NH3in", MCP)
# # NH3out = None
# # NH3in = None
# Thermero = Thermero_DS18B20("Thermero")
# # Thermero = None
# LCD = LCD_HD44780("LCD")
# try:
#     while True:
#         LCD.print_first(TrHin, TrHout, TrHamb, CO2in, CO2out, NH3in, NH3out)
#         print("-----------------------------")
#         time.sleep(8.0)
#         LCD.print_second(Flow, IRcamera, Thermero, Scale)
#         print("-----------------------------")
#         time.sleep(8.0)
# 
# except KeyboardInterrupt:
#     LCD.lcd.close(clear=True)
#     print("You have successfully terminated the programm.")