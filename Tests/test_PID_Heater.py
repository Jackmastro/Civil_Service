import RPi.GPIO as GPIO
from gpiozero import OutputDevice
from simple_pid import PID
import time
import board
import adafruit_ahtx0
import adafruit_tca9548a

# Set GPIO mode to BCM numbering
GPIO.setmode(GPIO.BCM)

# Set fan
Suct_fans = OutputDevice(23, active_high=False)

# Create I2C bus as normal
i2c = board.I2C()

# Create the TCA9548A (multiplexer) object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# Define AM2315 sensors connected to channels of the multiplexer
TrH_in = adafruit_ahtx0.AHTx0(tca[3])

# Set GPIO pin number
gpio_Heater = 12

# Set GPIO pin as output
GPIO.setup(gpio_Heater, GPIO.OUT)

# Set PWM frequency in Hz
pwm_frequency = 1
pwm_Heater = GPIO.PWM(gpio_Heater, pwm_frequency)

# Create PID controller
# Setpoint
T_Heater = 27

# PID parameters
Kp = 8
Ki = 0.01
Kd = 0

# Controller object
pid_Heater = PID(Kp, Ki, Kd, setpoint=T_Heater, output_limits=(0, 100))

try:
    Suct_fans.on()
    pwm_Heater.start(0)

    while True:
        pwm_output = pid_Heater(TrH_in.temperature)
        pwm_Heater.ChangeDutyCycle(pwm_output)

        print("Temperature:", round(TrH_in.temperature, 2), "°C")
        print("Duty cycle:", round(pwm_output, 2), "%")

        time.sleep(4.0)

except KeyboardInterrupt:
    print("You have successfully interrupted the programm.")

finally:
    Suct_fans.off()
    Suct_fans.close()
    pwm_Heater.stop()
    print("You have successfully cleaned the pins and turned off the heater.")