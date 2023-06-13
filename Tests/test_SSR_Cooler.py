from gpiozero import OutputDevice
import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM numbering
GPIO.setmode(GPIO.BCM)

# Set fan
Suct_fans = OutputDevice(23, active_high=False)

# Set GPIO pin number
gpio_Cooler_pin = 13

# Set GPIO pin as output
GPIO.setup(gpio_Cooler_pin, GPIO.OUT)

try:
    Suct_fans.on()

    Start_input = 'n'
    
    while Start_input != 'y':
    # Get the input from user
        Start_input = input("Do you want to start the Cooler? [y/n] \n")

        if Start_input == 'y':
            # Set GPIO pin to high
            GPIO.output(gpio_Cooler_pin, GPIO.HIGH)
            print("Cooler turned on")
        else:
            print("Cooler not started")
          
    Stop_input = 'n'
    
    while Stop_input != 'y':
        # Get the input from user
        Stop_input = input("Do you want to turn off the Cooler? [y/n] \n")

        if Stop_input == 'y':
            # Set GPIO pin to high
            GPIO.output(gpio_Cooler_pin, GPIO.LOW)
            print("Cooler turned off")
        else:
            print("Cooler still running")

        # Wait time
        time.sleep(5.0)

except KeyboardInterrupt:
    print("You have successfully interrupted the programm.")

finally:
    Suct_fans.off()
    Suct_fans.close()
    GPIO.output(gpio_Cooler_pin, GPIO.LOW)
    print("You have successfully cleaned the pins and turned off the cooler.")