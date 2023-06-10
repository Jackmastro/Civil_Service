# GENERAL IMPORT
import RPi.GPIO as GPIO
import datetime
import time

from LCD_Class import *
from Chip_Class import *
from Sensor_Class import *
from Actuator_Class import *
from Controller_Class import *
from Saver_Class import *

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

overview_sensor_dict = {
    "RTClock":   {"is_connected": True,  "sensor": None},
    "CO2in":     {"is_connected": True,  "sensor": None},
    "CO2out":    {"is_connected": True,  "sensor": None},
    "TrHout":    {"is_connected": True,  "sensor": None},
    "TrHin":     {"is_connected": True,  "sensor": None},
    "TrHamb":    {"is_connected": True,  "sensor": None},
    "TrHcool":   {"is_connected": True,  "sensor": None},
    "Flow":      {"is_connected": True,  "sensor": None},
    "NH3in":     {"is_connected": True,  "sensor": None},
    "NH3out":    {"is_connected": True,  "sensor": None},
    "Scale":     {"is_connected": False, "sensor": None},
    "IRcamera":  {"is_connected": False, "sensor": None},
    "Thermero":  {"is_connected": False, "sensor": None}
}

print("Needed to control the process:")
TCA = Multiplexer_TCA9548A("TCA")
TrHin = TrH_AM2315C("TrHin", TCA)
overview_sensor_dict["TrHin"]["sensor"] = TrHin
TrHout = TrH_AM2315C("TrHout", TCA)
overview_sensor_dict["TrHout"]["sensor"] = TrHout
TrHamb = TrH_AM2315C("TrHamb", TCA)
overview_sensor_dict["TrHamb"]["sensor"] = TrHamb
TrHcool = TrH_AM2315C("TrHcool", TCA)
overview_sensor_dict["TrHcool"]["sensor"] = TrHcool
print("Other sensors:")
print("Clock:")
RTClock = RTC_DS1307("RTClock")
overview_sensor_dict["RTClock"]["sensor"] = RTClock
CO2in = CO2_SCD30("CO2in", TCA)
overview_sensor_dict["CO2in"]["sensor"] = CO2in
CO2out = CO2_SCD30("CO2out", TCA)
overview_sensor_dict["CO2out"]["sensor"] = CO2out
Flow = Flow_SFM3119("Flow")
overview_sensor_dict["Flow"]["sensor"] = Flow
MCP = ADC_MCP3008("MCP")
NH3out = NH3_MQ137("NH3out", MCP)
NH3out = None
overview_sensor_dict["NH3out"]["sensor"] = NH3out
NH3in = NH3_MQ137("NH3in", MCP)
NH3in = None
print("Screen:")
lcd = LCD_HD44780("LCD")
print("Choosable sensors inside the chamber:")
# Scale
if is_connected("Scale"):
    overview_sensor_dict["Scale"]["is_connected"] = True
    Scale = Scale_HX711("Scale")
    overview_sensor_dict["Scale"]["sensor"] = Scale
else:
    Scale = None
# IR camera
if is_connected("IRcamera"):
    overview_sensor_dict["IRcamera"]["is_connected"] = True
    IRcamera = IR_MLX90640("IRcamera")
    overview_sensor_dict["IRcamera"]["sensor"] = IRcamera
else:
    IRcamera = None
# Thermero
if is_connected("Thermero"):
    overview_sensor_dict["Thermero"]["is_connected"] = True
    Thermero = Thermero_DS18B20("Thermero")
    overview_sensor_dict["Thermero"]["sensor"] = Thermero
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
rH_crit_max = 80

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
        saving_rate_min = max(save_rate_min, float(input_choice_save_rate))
        print("Save rate set:", saving_rate_min, "min")
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

######################## TODO CALL THE RTC
print("Saver:")
time_start_process_str = RTClock.read_data_point()
print(time_start_process_str)
saver = Saver(time_start_process_str)

print("TO STOP THE PROCESS: CTRL + C")

try:
    # Start the fans
    ventilation_fan.set_state(is_on=True)
    time.sleep(1) # Needed
    suction_fan.set_state(is_on=True)
    time.sleep(1) # Needed
    cooling_fan.set_state(is_on=True)
    time.sleep(1) # Needed

    # Initialize time variables
    time_last_save_LCD = time.time()
    display_rate = 5
    is_first_turn = True
    time_last_save_controller = time.time()
    control_rate = 2
    time_last_save_saving = time.time()
    saving_rate = saving_rate_min * 60 # Conversion to seconds

    while True:
        if time.time() - time_last_save_controller >= control_rate:
            controller.control(TrHamb, TrHin, TrHout, cooler, heater)

            # Update time variable
            time_last_save_controller = time.time()
            print("cont")
            print(heater.pwm_duty_cycle)
            print(TrHin.read_data_point())

        if time.time() - time_last_save_LCD >= display_rate:
            if is_first_turn:
                lcd.print_first(TrHin, TrHout, TrHamb, CO2in, CO2out, NH3in, NH3out)
                is_first_turn = not is_first_turn
            else:
                lcd.print_second(Flow, IRcamera, Thermero, Scale)
                is_first_turn = not is_first_turn
            
            # Update time variable
            time_last_save_LCD = time.time()
            print("lcd")
            
        if time.time() - time_last_save_saving >= saving_rate:
            saver.append_data(overview_sensor_dict)

            # Update time variable
            time_last_save_saving = time.time()
            print("sav")

except KeyboardInterrupt:
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
    print("--- CLEANUP COMPLETED ---")
    print("--- CSV GENERATION STARTED ---")
    saver.append_data(overview_sensor_dict)
    time.sleep(3)
    IRcamera.save_data()
    RTClock.save_data()
    time.sleep(3)
    IRcamera.save_data()
    RTClock.save_data()
    print("Last data saved.")
    saver.save_sensor_data(RTClock, TrHamb, TrHcool, TrHin, TrHout, CO2in, CO2out, NH3in, NH3out, Flow, Scale)
    saver.save_IR_data(RTClock, IRcamera)
    saver.save_Thermero_data(RTClock, Thermero)
    print("--- CSV GENERATION COMPLETED ---")
    print("--- PROGRAM TERMINATED ON {} ---".format(RTClock.read_data_point()))