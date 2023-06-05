import RPi.GPIO as GPIO
import time
from gpiozero import OutputDevice
import PID
import board
import adafruit_ahtx0
import adafruit_tca9548a

def setupRPi():
# Set temperature sensor
    # Create I2C bus as normal
    i2c = board.I2C()
    # Create the TCA9548A (multiplexer) object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)
    # Define AM2315 sensors connected to channels of the multiplexer
    TrH_in = adafruit_ahtx0.AHTx0(tca[3])

# Set PWM GPIO pin
    # Set GPIO mode to Board numbering
    GPIO.setmode(GPIO.BCM)
    # Set GPIO pin number
    gpio_Heater = 12
    # Set GPIO pin as output
    GPIO.setup(gpio_Heater, GPIO.OUT)
    # Set PWM frequency in Hz
    pwm_frequency = 1
    pwm_Heater = GPIO.PWM(gpio_Heater, pwm_frequency)

# Set PID controller
    # Controller object
    pid_Heater = PID()
    
    return TrH_in, pwm_Heater, pid_Heater