from abc import ABC, abstractmethod
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Actuator(ABC):
    def __init__(self, name=str) -> None:
        self.name = name
        self.state = False
        self.data_table = []
    
    @abstractmethod
    def set_state(self, is_on=False) -> None:
        pass

    @abstractmethod
    def save_data_point(self) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

class Fan(Actuator):
    def __init__(self, name):
        super().__init__(name)

        pin_mapping = {
            'Ventilation': 24, #18
            'Suction': 23, #16
            'Cooling': 22 #15
        }

        if self.name not in pin_mapping:
            raise ValueError('name has to be "Ventilation", "Suction" or "Cooling". Received: {}'.format(self.name))

        self.gpio_BCM = pin_mapping[self.name]
        GPIO.setup(self.gpio_BCM, GPIO.OUT)
        GPIO.output(self.gpio_BCM, GPIO.HIGH)

        print(f"Setup for {self.name} successfully completed.")

    def set_state(self, is_on):
        if not isinstance(is_on, bool):
            raise ValueError('is_on has to be a boolean value. Received: {}'.format(is_on))

        self.state = is_on
        GPIO.output(self.gpio_BCM, GPIO.LOW if is_on else GPIO.HIGH)
    
    def save_data_point(self):
        self.data_table.append(self.state)

    def cleanup(self):
        GPIO.output(self.gpio_BCM, GPIO.HIGH)

        print(f"Cleanup for {self.name} successfully completed.")

class Cooler(Actuator):
    def __init__(self, name=str) -> None:
        super().__init__(name)

        self.gpio_Cooler_BCM = 13 #33
        GPIO.setup(self.gpio_Cooler_BCM, GPIO.OUT)
        GPIO.output(self.gpio_Cooler_BCM, GPIO.LOW)

        print(f"Setup for {self.name} successfully completed.")

    def set_state(self, is_on):
        if not isinstance(is_on, bool):
            raise ValueError('is_on has to be a boolean value. Received: {}'.format(is_on))

        self.state = is_on
        GPIO.output(self.gpio_Cooler_BCM, GPIO.HIGH if is_on else GPIO.LOW)

    def save_data_point(self):
        self.data_table.append(self.state)

    def cleanup(self):
        GPIO.output(self.gpio_Cooler_BCM, GPIO.LOW)

        print(f"Cleanup for {self.name} successfully completed.")

class Heater(Actuator):
    def __init__(self, name=str) -> None:
        super().__init__(name)
        
        gpio_Heater_BCM = 12 #32
        GPIO.setup(gpio_Heater_BCM, GPIO.OUT)

        pwm_frequency = 1 # Hz
        self.pwm_duty_cycle = 0 # %
        self.PWM = GPIO.PWM(gpio_Heater_BCM, pwm_frequency)

        print(f"Setup for {self.name} successfully completed.")

    def set_state(self, is_on):
        if not isinstance(is_on, bool):
            raise ValueError('is_on has to be a boolean value. Received: {}'.format(is_on))

        self.state = is_on

        if is_on:
            self.PWM.start(self.pwm_duty_cycle)
        else:
            self.pwm_duty_cycle = 0
            self.PWM.stop()

    def save_data_point(self):
        self.data_table.append(self.pwm_duty_cycle)

    def set_duty_cycle(self, duty_cycle) -> None:
        if not isinstance(duty_cycle, float) or not 0 <= duty_cycle <= 100:
            raise ValueError('duty_cycle has to be a float between 0 and 100. Received: {}'.format(duty_cycle))

        self.pwm_duty_cycle = duty_cycle
        self.PWM.ChangeDutyCycle(duty_cycle)

    def cleaunup(self):
        self.PWM.stop()

        print(f"Cleanup for {self.name} successfully completed.")

###############################################################################
# cooler = Cooler("Cooler")
# 
# try:
#     Start_input = 'n'
#     
#     while Start_input != 'y':
#         # Get the input from user
#         Start_input = input("Do you want to start the Cooler? [y/n] \n")
# 
#         if Start_input == 'y':
#             # Set GPIO pin to high
#             cooler.set_state("On")
#             print("Cooler turned on")
#         else:
#             print("Cooler not started")
#           
#     Stop_input = 'n'
#     
#     while Stop_input != 'y':
#         # Get the input from user
#         Stop_input = input("Do you want to turn off the Cooler? [y/n] \n")
# 
#         if Stop_input == 'y':
#             # Set GPIO pin to high
#             cooler.set_state("Off")
#             print("Cooler turned off")
#         else:
#             print("Cooler still running")
# 
#         # Wait time
#         time.sleep(5.0)
# 
# except KeyboardInterrupt:
#     print("\nKeyboard Interrupt: End program")
#     
# finally:
#     cooler.set_state("Off")
#     # Clean up GPIO
# #     GPIO.cleanup()

######################################################################################
# heater = Heater("Heater")

# try:
#     Start_input = 'n'
    
#     while Start_input != 'y':
#         # Get the input from user
#         Start_input = input("Do you want to start the Heater? [y/n] \n")

#         if Start_input == 'y':
#             # Set GPIO pin to high
#             heater.set_state("On")
#             print("Heater turned on")
#         else:
#             print("Heater not started")
            
#     while True:
#         # Get the input from user
#         PWM_input = int(input("What duty cycle in percentage from 0 to 99 do you want? \n"))

#         # Check if the input is an int between 0 and 100 %
#         if isinstance(PWM_input, int) and 0 <= PWM_input < 100:
#             # Change duty cycle
#             heater.set_duty_cycle(PWM_input)
#             print("Duty cycle changed to", PWM_input)
            
#         elif isinstance(PWM_input, int) and PWM_input == 100:
#             # Change duty cycle
#             heater.set_duty_cycle(PWM_input)
#             print("Duty cycle changed to", PWM_input)
#             break
        
#         else:
#             print("Please enter a valid integer between 0 and 99.")
          
#     Stop_input = 'n'
    
#     while Stop_input != 'y':
#         # Get the input from user
#         Stop_input = input("Do you want to turn off the Heater? [y/n] \n")

#         if Stop_input == 'y':
#             # Set GPIO pin to high
#             heater.set_state("Off")
#             print("Heater turned off")
#         else:
#             print("Heater still running")

#         # Wait time
#         time.sleep(5.0)

# except KeyboardInterrupt:
#     print("\nKeyboard Interrupt: End program")
    
# finally:
#     heater.set_state("Off")
#     # Clean up GPIO
# #     GPIO.cleanup()

###########################################################################################
# fan = Fan("Ventilation")
# fan = Fan("Suction")
# fan = Fan("Cooling")

# try:
#     Start_input = 'n'
    
#     while Start_input != 'y':
#         # Get the input from user
#         Start_input = input(f"Do you want to start the {fan.name}? [y/n] \n")

#         if Start_input == 'y':
#             # Set GPIO pin to high
#             fan.set_state("On")
#             print(f"{fan.name} turned on")
#         else:
#             print(f"{fan.name} not started")
          
#     Stop_input = 'n'
    
#     while Stop_input != 'y':
#         # Get the input from user
#         Stop_input = input(f"Do you want to turn off the {fan.name}? [y/n] \n")

#         if Stop_input == 'y':
#             # Set GPIO pin to high
#             fan.set_state("Off")
#             print(f"{fan.name} turned off")
#             break
#         else:
#             print(f"{fan.name} still running")

#         # Wait time
#         time.sleep(5.0)

# except KeyboardInterrupt:
#     fan.set_state("Off")
#     print("\nKeyboard Interrupt: End program")
    
# finally:
#     fan.set_state("Off")
#     # Clean up GPIO
# #     GPIO.cleanup()