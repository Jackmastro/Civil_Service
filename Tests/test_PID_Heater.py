import RPi.GPIO as GPIO
import time
from gpiozero import OutputDevice
from simple_pid import PID
import board
import adafruit_ahtx0
import adafruit_tca9548a

# Set GPIO mode to Board numbering
GPIO.setmode(GPIO.BCM)

# Set fan
Suct_fans = OutputDevice(23, active_high=False)
Suct_fans.on()

# Set temperature sensor
# Create I2C bus as normal
i2c = board.I2C()
# Create the TCA9548A (multiplexer) object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)
# Define AM2315 sensors connected to channels of the multiplexer
TrH_in = adafruit_ahtx0.AHTx0(tca[3])

# Set PWM GPIO pin
# Set GPIO pin number
gpio_Heater = 12
# Set GPIO pin as output
GPIO.setup(gpio_Heater, GPIO.OUT)
# Set PWM frequency in Hz
pwm_frequency = 1
pwm_Heater = GPIO.PWM(gpio_Heater, pwm_frequency)

pwm_Heater.start(0)
# Create PID controller
# Setpoint
T_Heater = 27 
# PID parameters
Kp = 5
Ki = 0.01
Kd = 0
# Controller object
pid_Heater = PID(Kp, Ki, Kd, setpoint=T_Heater)

try:
    while True:
        # Get and apply actuator PID computed duty cycle 
        pwm_output = pid_Heater(TrH_in.temperature)
        
        # Just an initial check
        print("Temperature:", round(TrH_in.temperature,2), "°C")
        print("Duty cycle:", round(pwm_output,2), "%")
        
        pwm_Heater.ChangeDutyCycle(pwm_output)
        
        # Wait time
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nKeyboard Interrupt: Heater stopped")

finally:
    # Stop fan
    Suct_fans.off()
    Suct_fans.close()
    # Stop PWM
    pwm_Heater.stop()
    print("\nEnd program")
