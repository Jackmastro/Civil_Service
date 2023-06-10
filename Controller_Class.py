# General imports
import RPi.GPIO as GPIO

# Psychrometric conversion library https://github.com/psychrometrics/psychrolib (Installation: https://pypi.org/project/PsychroLib/, Documentation: https://psychrometrics.github.io/psychrolib/api_docs.html)
import psychrolib
# Simple PID library https://github.com/m-lundberg/simple-pid/tree/master (Documentation: https://pypi.org/project/simple-pid/)
from simple_pid import PID

# Import the Sensor abstract class
from Sensor_Class import *
# Import the Actuator abstract class
from Actuator_Class import *

class Controller():
    def __init__(self, name=str, Tref_in=float, Tref_out=float, rH_crit=float) -> None:
        self.name = name
        self.Tref_in = Tref_in
        self.Tref_out = Tref_out
        self.rH_crit = rH_crit
        self.w_in_crit = self.calculate_humidity_ratio(rH_crit, Tref_in)
        self.w_out_crit = self.calculate_humidity_ratio(rH_crit, Tref_out)

        self.previous_dict = {
            'cooler_state': False,
            'heater_state': False,
            'heater_Tref': None,
            'phase': None
        }
        self.next_dict = {
            'cooler_state': False,
            'heater_state': False,
            'heater_Tref': None,
            'phase': None
        }

        # Set PID objects with ARW = Anti Reset Windup for the duty cycle [0-100]
        self.pid_heater_chill = PID(Kp=7.0, Ki=0.008, Kd=0.0, output_limits=(0, 100))
        self.pid_heater_peak = PID(Kp=2.0, Ki=0.001, Kd=0.0, output_limits=(0, 100))

        print(f"Setup for {self.name} successfully completed.")
    
    def calculate_humidity_ratio(self, relative_humidity=float, temperature=float) -> float:
        pressure = 101325.0  # Pa
        psychrolib.SetUnitSystem(psychrolib.SI)
        return psychrolib.GetHumRatioFromRelHum(TDryBulb=temperature, RelHum=relative_humidity/100, Pressure=pressure)
    
    def read_data_from_sensors(self, TrHamb, TrHin, TrHout) -> None:
        self.T_amb_value, self.rH_amb_value = TrHamb.read_data()
        self.T_out_value, self.rH_out_value = TrHout.read_data()
        self.T_in_value, _ = TrHin.read_data()

    def state_machine(self) -> dict:
        # CHILL PHASE
        if self.T_out_value <= self.Tref_out and self.rH_out_value <= self.rH_crit:
            # Cooling + Heating
            if self.w_amb_value >= self.w_in_crit:
                print("Chill: Cooling + Heating")
                return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_in, 'phase': "chill"}
            else:
                # Heating
                if self.T_amb_value <= self.Tref_in:
                    print("Chill: Heating")
                    return {'cooler_state': False, 'heater_state': True, 'heater_Tref': self.Tref_in, 'phase': "chill"}
                # Cooling (+ Heating)
                else:
                    print("Chill: Cooling + (Heating)")
                    return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_in, 'phase': "chill"}
        #PEAK PHASE
        elif self.T_out_value >= self.Tref_out or self.rH_out_value >= self.rH_crit:
            # Cooling + Heating
            if self.w_out_value >= self.w_out_crit:
                print("Peak: Cooling + Heating")
                return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_out, 'phase': "peak"}
            else:
                # Heating
                if self.T_out_value <= self.Tref_out:
                    print("Peak: Heating")
                    return {'cooler_state': False, 'heater_state': True, 'heater_Tref': self.Tref_out, 'phase': "peak"}
                # Cooling (+ Heating)
                else:
                    print("Peak: Cooling + (Heating)")
                    return {'cooler_state': True, 'heater_state': True, 'heater_Tref': self.Tref_out, 'phase': "peak"}

    def control(self, TrHamb, TrHin, TrHout, cooler, heater) -> None:
        print("inside control")
        # Read data from sensors
        self.read_data_from_sensors(TrHamb, TrHin, TrHout)

        # Calculate the humdity ratios of interest
        self.w_amb_value = self.calculate_humidity_ratio(self.rH_amb_value, self.T_amb_value)
        self.w_out_value = self.calculate_humidity_ratio(self.rH_out_value, self.T_out_value)

        # Call the state machine
        self.next_dict = self.state_machine()

        # Set Actuators when the state changes
        if self.next_dict['cooler_state'] != self.previous_dict['cooler_state']:
            # Set the Cooler
            cooler.set_state(self.next_dict['cooler_state'])

        if self.next_dict['heater_state'] != self.previous_dict['heater_state']:
            # Set the Heater
            heater.set_state(self.next_dict['heater_state'])
            # Update temperature reference
            if self.next_dict['heater_state']:
                if self.next_dict['phase'] == "chill":
                    self.pid_heater_chill.setpoint = self.next_dict['heater_Tref']
                elif self.next_dict['phase'] == "peak":
                    self.pid_heater_peak.setpoint = self.next_dict['heater_Tref']
                else:
                    raise ValueError('phase has to be "chill" or "peak". Received: {}'.format(self.next_dict['phase']))

        # Call the PID controllers
        if self.next_dict['heater_state']:
            if self.next_dict['phase'] == "chill":
                duty_cycle = self.pid_heater_chill(self.T_in_value)
            elif self.next_dict['phase'] == "peak":
                duty_cycle = self.pid_heater_peak(self.T_out_value)
            else:
                raise ValueError('phase has to be "chill" or "peak". Received: {}'.format(self.next_dict['phase']))
            
        print(self.previous_dict)
        duty_cycle = round(float(duty_cycle), 2)
        heater.set_duty_cycle(duty_cycle)

        # Update dictionaries
        self.previous_dict = self.next_dict
        print(self.next_dict)