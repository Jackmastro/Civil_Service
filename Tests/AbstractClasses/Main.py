# GENERAL IMPORT
import RPi.GPIO as GPIO
import numpy as np
import time
import csv

from LCD_Class import *
from Chip_Class import *
from Sensor_Class import *
from Actuator_Class import *
from Controller_Class import *
# from Saver_Class import *

GPIO.setmode(GPIO.BCM)

def is_connected(name=str) -> bool:
    while True:
        input_sensor_connected = input(f"Is the {name} connected to read data? [y/n]: ")
        
        if input_sensor_connected == 'y':
            print(f"{name} is connected.")
            return True
        elif input_sensor_connected == 'n':
            print(f"{name} is not connected.")
            return False
        else:
            print("Wrong choice. Please enter either 'y' or 'n'.")

############################################################################
print("--- PROGRAM STARTED ---")
print("--- SENSOR INITIALIZATION ---")
is_connected_dict = {
    "CO2in"    : True,
    "CO2out"   : True,
    "TrHout"   : True,
    "TrHin"    : True,
    "TrHamb"   : True,
    "TrHcool"  : True,
    "Flow"     : True,
    "NH3in"    : True,
    "NH3out"   : True,
    "RTClock"  : True,
    "Scale"    : False,
    "IRcamera" : False,
    "Thermero" : False
}

print("Needed to control the process:")
TCA = Multiplexer_TCA9548A("TCA")
TrHin = TrH_AM2315C("TrHin", TCA)
TrHout = TrH_AM2315C("TrHout", TCA)
TrHamb = TrH_AM2315C("TrHamb", TCA)
TrHcool = TrH_AM2315C("TrHcool", TCA)
print("Other sensors:")
CO2in = CO2_SCD30("CO2in", TCA)
CO2out = CO2_SCD30("CO2out", TCA)
Flow = Flow_SFM3119("Flow")
MCP = ADC_MCP3008("MCP")
NH3out = NH3_MQ137("NH3out", MCP)
NH3in = NH3_MQ137("NH3in", MCP)
NH3out = None
NH3in = None
print("Clock:")
# RTClock = RTC_DS1307("RTClock")
print("Screen:")
lcd = LCD_HD44780("LCD")
print("Choosable sensors inside the chamber:")
# Scale
if is_connected("Scale"):
    is_connected_dict["Scale"] = True
    Scale = Scale_HX711("Scale")
else:
    Scale = None
# IR camera
if is_connected("IRcamera"):
    is_connected_dict["IRcamera"] = True
    IRcamera = IR_MLX90640("IRcamera")
else:
    IRcamera = None
# Thermero
if is_connected("Thermero"):
    is_connected_dict["Thermero"] = True
    Thermero = Thermero_DS18B20("Thermero")
else:
    Thermero = None

print("--- SENSOR INITIALIZATION COMPLETED ---")
############################################################################
print("--- ACTUATOR INITIALIZATION ---")

print("Fans:")
ventilation_fan = Fan("Ventilation")
suction_fan = Fan("Suction")
cooling_fan = Fan("Cooling")
print("Cooler:")
cooler = Cooler("Cooler")
print("Heater:")
heater = Heater("Heater")

print("--- ACTUATOR INITIALIZATION COMPLETED ---")
############################################################################
print("--- PARAMETERS INITIALIZATION ---")
# Input reference temperature in °C
Tref_in_min = 20
Tref_in_max = 35

while True:
    input_choice_Tref_in = input("What reference TEMPERATURE in °C do you want at the INLET of the chamber? [from {} to {}] ".format(Tref_in_min, Tref_in_max))
    
    try:
        Tref_in = float(input_choice_Tref_in)
        if Tref_in_min <= Tref_in <= Tref_in_max:
            print("Inlet reference temperature set:", Tref_in, "°C")
            break  # Exit the loop if a valid input is provided
        else:
            print("Input out of range. Please enter a value within the specified range.")
    except ValueError:
        print("Invalid input. Please enter a valid float value.")

# Output reference temperature in °C
Tref_out_min = 20
Tref_out_max = 35

while True:
    input_choice_Tref_out = input("What reference TEMPERATURE in °C do you want at the OUTLET of the chamber? [from {} to {}] ".format(Tref_out_min, Tref_out_max))
    
    try:
        Tref_out = float(input_choice_Tref_out)
        if Tref_out_min <= Tref_out <= Tref_out_max:
            print("Outlet reference temperature set:", Tref_out, "°C")
            break  # Exit the loop if a valid input is provided
        else:
            print("Input out of range. Please enter a value within the specified range.")
    except ValueError:
        print("Invalid input. Please enter a valid float value.")

# Critical relative humidity in %
rH_crit_min = 50
rH_crit_max = 90

while True:
    input_choice_rH_crit = input("What critical RELATIVE HUMIDITY in %% do you want at the INLET of the chamber? [from {} to {}] ".format(rH_crit_min, rH_crit_max))
    
    try:
        rH_crit = float(input_choice_rH_crit)
        if rH_crit_min <= rH_crit <= rH_crit_max:
            print("Critical relative humidity set:", rH_crit, "%")
            break  # Exit the loop if a valid input is provided
        else:
            print("Input out of range. Please enter a value within the specified range.")
    except ValueError:
        print("Invalid input. Please enter a valid float value.")

# Initialize controller
print("Controller:")
controller = Controller("Controller", Tref_in, Tref_out, rH_crit)

# Saving rate in minutes
save_rate_min = 1

while True:
    input_choice_save_rate = input("How often do you want to SAVE the data in minutes? [from {}] ".format(save_rate_min))
    
    try:
        save_rate = max(save_rate_min, float(input_choice_save_rate))
        print("Save rate set:", save_rate, "min")
        break  # Exit the loop if a valid input is provided
    except ValueError:
        print("Invalid input. Please enter a valid float value.")

print("--- PARAMETERS INITIALIZATION COMPLETED ---")
############################################################################
print("--- PROCESS ---")
process_is_started = False

while not process_is_started:
    input_want_process_start = input("Do you want to start the process? [y/n]: ")

    if input_want_process_start == 'y':
        process_is_started = True
        print("Process started.")
    elif input_want_process_start == 'n':
        print("Process not started.")
    else:
        print("Wrong choice. Please enter either 'y' or 'n'.")

print("TO STOP THE PROCESS: CTRL + C")

try:
    # Start the fans
    ventilation_fan.set_state(is_on=True)
    time.sleep(1)
    suction_fan.set_state(is_on=True)
    time.sleep(1)
    cooling_fan.set_state(is_on=True)
    time.sleep(1)

    timestamp_LCD = time.time()
    display_rate = 5
    is_first_turn = True
    timestamp_controller = time.time()
    control_rate = 2
    timestamp_save = time.time()
    saving_rate = save_rate / 60 # converted to seconds
    #########TODO LIST TO SAVE THE TIMESTAMPS

    while True:
        print(heater.pwm_duty_cycle)
        print(TrHin.read_data_point())
        time.sleep(3)
        
        if time.time() - timestamp_LCD >= display_rate:
            if is_first_turn:
                lcd.print_first(TrHin, TrHout, TrHamb, CO2in, CO2out, NH3in, NH3out)
                is_first_turn = not is_first_turn
            else:
                lcd.print_second(Flow, IRcamera, Thermero, Scale)
                is_first_turn = not is_first_turn
                
            timestamp_LCD = time.time()

        if time.time() - timestamp_controller >= control_rate:
            controller.control(TrHamb, TrHin, TrHout, cooler, heater)
                
            timestamp_controller = time.time()
            
        if time.time() - timestamp_save >= saving_rate:
            ##TODO
            #### UPDATE TIMESTAMP LIST
            timestamp_save = time.time()

except KeyboardInterrupt:
    ################TODO 
    # call the saver for last point
    print("Last data saved.")
    print("--- PROCESS TERMINATED ---")

finally:
    print("--- CLEANUP STARTED ---")
    ventilation_fan.cleanup()
    suction_fan.cleanup()
    cooling_fan.cleanup()
    cooler.cleanup()
    heater.cleanup()
    lcd.cleanup()
    # NOT GPIO.cleanup(), the heater and cooler will turn on!
    ################# FIND OUT HOW TO IMPLEMENT ACTIVE=LOW SO THAT THEY WILL TURN OFF WHEN CLEANUP IS CALLED
    print("--- CLEANUP COMPLETED ---")
    print("--- PROGRAM TERMINATED ---")
    