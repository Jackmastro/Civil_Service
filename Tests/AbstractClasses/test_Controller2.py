from simple_pid import PID
import RPi.GPIO as GPIO
from test_Sensor import *
from test_Actuator import *
from test_Chip import *

class Controller():
    def __init__(self, Tref_in=float, Tref_out=float, rH_crit=float) -> None:
        self.heater_state = "Off"
        self.cooler_state = "Off"
        self.T_heater_ref
        self.Tref_in = Tref_in
        self.Tref_out = Tref_out
        self.rH_crit = rH_crit
        self.rHin_crit = 0.0135
        self.rHout_crit = 0.0180
    
    def start(self, TrHamb, TrHin, TrHout):
        # Get data
        TrH_amb_value = TrHamb.read_data()
        TrH_in_value = TrHin.read_data()
        TrH_out_value = TrHout.read_data()

        # Set reference
        [self.T_ref, self.rH_ref, self.heater_state, self.cooler_state] = self.set_references(TrH_amb_value, TrH_in_value, TrH_out_value)
        # Get and set output
        return 

    def set_references(self, TrH_amb_value, TrH_in_value, TrH_out_value):
        # Chill phase
        if TrH_out_value[0] <= self.Tref_out and TrH_out_value[1] <= self.rHout_crit: 
            if TrH_amb_value[1] > self.rHin_crit:
                self.heater_state = "On"
                self.cooler_state = "On"
                self.T_heater_ref = self.Tref_in
            else:
                if TrH_amb_value[0] <= self.Tref_in: 
                    self.heater_state = "On"
                    self.T_heater_ref = self.Tref_in
                else:
                    self.heater_state = "On"
                    self.cooler_state = "On"
                    self.T_heater_ref = self.Tref_in
        # Peak phase
        elif TrH_out_value[0] >= self.Tref_out or TrH_out_value[1] >= self.rHout_crit: 
            if TrH_amb_value[1] > self.rHin_crit:
                self.heater_state = "On"
                self.cooler_state = "On"
                self.T_heater_ref = self.Tref_in
            else:
                if TrH_amb_value[0] <= self.Tref_in: 
                    self.heater_state = "On"
                    self.T_heater_ref = self.Tref_in
                else:
                    self.heater_state = "On"
                    self.cooler_state = "On"
                    self.T_heater_ref = self.Tref_in
    
    
    
    
    
    