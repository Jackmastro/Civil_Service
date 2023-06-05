# General imports
import RPi.GPIO as GPIO

# Psychrometric conversion library https://github.com/psychrometrics/psychrolib (Installation: https://pypi.org/project/PsychroLib/, Documentation: https://psychrometrics.github.io/psychrolib/api_docs.html)
import psychrolib
# Simple PID library https://github.com/m-lundberg/simple-pid/tree/master (Documentation: https://pypi.org/project/simple-pid/)
from simple_pid import PID

# Import the Sensor abstract class
from test_Sensor import *
# Import the Actuator abstract class
from test_Actuator import *

class Controller():
    def __init__(self, name=str, Tref_in=float, Tref_out=float, rH_crit=float) -> None:
        self.name = name
        self.Tref_in = Tref_in
        self.Tref_out = Tref_out
        self.rH_crit = rH_crit
        self.w_in_crit = self.calculate_humidity_ratio(rH_crit, Tref_in) #0.0135
        self.w_out_crit = self.calculate_humidity_ratio(rH_crit, Tref_out) #0.0180

        self.previous_dict = {
            'cooler_state': False,
            'heater_state': False,
            'heater_Tref': None
        }
        self.next_dict = {
            'cooler_state': False,
            'heater_state': False,
            'heater_Tref': None
        }

        # PID parameters
        Kp = 8.0
        Ki = 0.01
        Kd = 0

        # Set PID object with ARW = Anti Reset Windup for the duty cycle [0-100]
        self.pid_heater = PID(Kp, Ki, Kd, output_limits=(0, 100))

        print(f"Setup for {self.name} successfully completed.")
    
    def calculate_humidity_ratio(self, relative_humidity=float, temperature=float) -> float:
        pressure = 101325.0  # Pa
        psychrolib.SetUnitSystem("SI")
        return psychrolib.GetHumRatioFromRelHum(TDryBulb=temperature, RelHum=relative_humidity/100, Pressure=pressure)
    
    def read_data_from_sensors(self, TrHamb, TrHin, TrHout) -> None:
        self.T_amb_value, self.rH_amb_value = TrHamb.read_data()
        self.T_out_value, self.rH_out_value = TrHout.read_data()
        self.T_in_value = TrHin.read_data_point()

    def state_machine(self) -> dict:
        # CHILL PHASE
        if self.T_out_value <= self.Tref_out and self.rH_out_value <= self.rH_crit:
            # Cooling + Heating
            if self.w_amb_value >= self.w_in_crit:
                return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_in}
            else:
                # Heating
                if self.T_amb_value <= self.Tref_in:
                    return {'cooler_state': False, 'heater_state': True, 'heater_Tref': self.Tref_in}
                # Cooling (+ Heating)
                else:
                    return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_in}
        #PEAK PHASE
        elif self.T_out_value >= self.Tref_out or self.rH_out_value >= self.rH_crit:
            # Cooling + Heating
            if self.w_out_value >= self.w_out_crit:
                return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_out}
            else:
                # Heating
                if self.T_out_value <= self.Tref_out:
                    return {'cooler_state': False, 'heater_state': True, 'heater_Tref': self.Tref_out}
                # Cooling (+ Heating)
                else:
                    return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_out}

    def control(self, TrHamb, TrHin, TrHout, cooler, heater) -> None:
        # Read data from sensors
        self.read_data_from_sensors(TrHamb, TrHin, TrHout)

        # Calculate the humdity ratios of interest
        self.w_amb_value = self.calculate_humidity_ratio(self.rH_amb_value, self.T_amb_value)
        self.w_out_value = self.calculate_humidity_ratio(self.rH_out_value, self.T_out_value)

        # Call the state machine
        self.next_dict = self.state_machine()

        # Call the Cooler
        if self.next_dict['cooler_state'] != self.previous_dict['cooler_state']:
            cooler.set_state(self.next_dict['cooler_state'])

        # Call the Heater
        if self.next_dict['heater_state'] != self.previous_dict['heater_state']:
            heater.set_state(self.next_dict['heater_state'])

            # Update temperature reference
            if self.next_dict['heater_state']:
                self.pid_heater.setpoint = self.next_dict['heater_Tref']
        
        # Call the PID controller
        if self.next_dict['heater_state']:
            duty_cycle = self.pid_heater(self.T_in_value)
            heater.set_duty_cycle(duty_cycle)

        # Update dictionaries
        self.previous_dict = self.next_dict