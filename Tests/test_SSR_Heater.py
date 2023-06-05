import RPi.GPIO as GPIO
import time
from gpiozero import OutputDevice

Suct_fans = OutputDevice(22, active_high=False)

# Set GPIO mode to Board numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO pin number
gpio_Heater_pin = 12

# # Set GPIO pin number
# gpio_Fan_pin = 38

# Set GPIO pin as output
GPIO.setup(gpio_Heater_pin, GPIO.OUT)

# # Set GPIO pin as output
# GPIO.setup(gpio_Fan_pin, GPIO.OUT)

#         # Set GPIO pin to high
#         GPIO.output(gpio_Fan_pin, GPIO.HIGH)
Suct_fans.on()

# Set PWM frequency in Hz
pwm_frequency = 1
pwm_Heater = GPIO.PWM(gpio_Heater_pin, pwm_frequency)

# Set PWM duty cycle in %
pwm_dutyCycle = 10

try:
    Start_input = 'n'
    
    while Start_input != 'y':
    # Get the input from user
        Start_input = input("Do you want to start the Heater? [y/n] \n")

    # Check if the input
        if Start_input == 'y':
        # Set GPIO pin to high
#             GPIO.output(gpio_Heater_pin, GPIO.HIGH)
            pwm_Heater.start(pwm_dutyCycle)
        
            print("Heater started")
        else:
            print("Heater not started")
    
    while True:
        # Get the input from user
        PWM_input = int(input("What duty cycle in percentage from 0 to 100 do you want? \n"))

        # Check if the input is an int between 0 and 100 %
        if isinstance(PWM_input, int) and 0 <= PWM_input <= 100:
            # Change duty cycle
            pwm_Heater.ChangeDutyCycle(PWM_input)
            print("Duty cycle changed to", PWM_input)
        else:
            print("Please enter a valid integer between 0 and 100.")

        # Wait time
        time.sleep(5.0)

except KeyboardInterrupt:
#     # Set GPIO pin to high
#     GPIO.output(gpio_Fan_pin, GPIO.LOW)
    Suct_fans.off()
    
    # Stop PWM
    pwm_Heater.stop()

    # Clean up GPIO
    GPIO.cleanup()

    print("\nKeyboard Interrupt: End program")