# pip install mcp3008
# https://tutorials-raspberrypi.com/configure-and-read-out-the-raspberry-pi-gas-sensor-mq-x/

import time
import math
import adafruit_mcp3xxx.mcp3008 as mcp3008
from adafruit_mcp3xxx.analog_in import AnalogIn

class MQ137:

    # Hardware Related Macros
    RL_VALUE                     = 5.6      # Define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 1        # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO, which is derived from the chart in datasheet from the air sensitivty curve
 
    # Software Related Macros 
    CALIBRATION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interval(in milisecond) between each samples in the cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation normal operation
 

    def __init__(self, adc, Ro=10, analogPin=0):      # Default values that can be changed (necessary for the calibration). Ro has to be changed after calibration
        self.adc = adc
        self.Ro = Ro
        self.channel = self.init_channel(analogPin)
        
        # NH3 sensitivity curve parameter: log(y) = m * log(x) + q
        self.m = -0.0024
        self.q = math.log(0.582) - self.m * math.log(1)  

    def init_channel(self, analogPin):
        if analogPin == 0:
            self.channel = AnalogIn(self.adc, mcp3008.P0)
        elif analogPin == 1:
            self.channel = AnalogIn(self.adc, mcp3008.P1)
        else:
            print("Invalid analogPin number. Check init_channel function!")
        return self.channel

    
    # MQResistanceCalculation
    # Input:   raw_adc - raw (voltage) value read from adc
    # Output:  measured sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage across the load resistor and its resistance, the resistance of the sensor can be derived.
 
    def MQResistanceCalculation(self, raw_adc):
#         65472.0
        return float(self.RL_VALUE*(65472.0-raw_adc)/float(raw_adc));
     
     
    # MQCalibration
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It uses MQResistanceCalculation to calculates the sensor resistance in clean air.
    
    def MQCalibration(self):
        Ro = 0.0
        for i in range(self.CALIBRATION_SAMPLE_TIMES):          # take multiple samples
            Ro += self.MQResistanceCalculation(self.channel.value)
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)      
        Ro = Ro/self.CALIBRATION_SAMPLE_TIMES                 # calculate the average value
        Ro = Ro/self.RO_CLEAN_AIR_FACTOR
        return Ro
     
    # MQGetGasPercentage 
    # Input:   Rs_Ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function converts the resistence into ppm.

    def MQGetGasPercentage(self):
        Rs = self.MQRead()
        Rs_Ro_ratio = Rs/self.Ro
        return self.MQGetPercentage(Rs_Ro_ratio)
     
    # MQRead
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
 
    def MQRead(self):
        Rs = 0.0
        for i in range(self.READ_SAMPLE_TIMES):
            Rs += self.MQResistanceCalculation(self.channel.value)
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)
        Rs = Rs/self.READ_SAMPLE_TIMES
        return Rs 
    
    # MQGetPercentage 
    # Input:   Rs_Ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) of the line could be derived if y(rs_ro_ratio) is provided.
 
    def MQGetPercentage(self, Rs_Ro_ratio):
        return math.pow(10, (math.log(Rs_Ro_ratio) - self.q) / self.m)
    