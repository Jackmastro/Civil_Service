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
Suct_fans = OutputDevice(19, active_high=False)
Suct_fans.on()

# Set temperature sensor
# Create I2C bus as normal
i2c = board.I2C()
# Create the TCA9548A (multiplexer) object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)
# Define AM2315 sensors connected to channels of the multiplexer
TrH_cool = adafruit_ahtx0.AHTx0(tca[5])
TrH_amb = adafruit_ahtx0.AHTx0(tca[4])
TrH_in = adafruit_ahtx0.AHTx0(tca[3])

# Set PWM GPIO pin
# Set GPIO pin number
gpio_Cooler = 13
# Set GPIO pin as output
GPIO.setup(gpio_Cooler, GPIO.OUT)


# Set PWM frequency in Hz
pwm_frequency = 1/120
pwm_Cooler = GPIO.PWM(gpio_Cooler, pwm_frequency)

# Create PID controller
# Setpoint
T_Cooler = 23
# PID parameters
Kp = -1
Ki = 0
Kd = 0
# Controller object
pid_Cooler = PID(Kp, Ki, Kd, setpoint=T_Cooler)

try:
    minute = 0
    while True:
        
        # Get and apply actutor PID computed duty cycle 
        pwm_output = pid_Cooler(TrH_cool.temperature)
        
        if pwm_output > 100:
            pwm_output = 100
        elif pwm_output < 0:
            pwm_output = 0
        else:
            pass

        pwm_Cooler.ChangeDutyCycle(pwm_output)
        
        print("DutyCylce:", round(pwm_output,2), "%")
        print("AMB T:", round(TrH_amb.temperature,2), "°C")
        print("AMB rH:", round(TrH_amb.relative_humidity,2), "%")
        print("COOL T:", round(TrH_cool.temperature,2), "°C")
        print("COOL rH:", round(TrH_cool.relative_humidity,2), "%")
        print("IN T:", round(TrH_in.temperature,2), "°C")
        print("IN rH:", round(TrH_in.relative_humidity,2), "%")
        print("-----------------", minute, "----------------------------")
        minute += 2 
        time.sleep(120.0)

except KeyboardInterrupt:
    # Stop fan
    Suct_fans.off()
    Suct_fans.close()
    # Turn off cooler
    GPIO.output(gpio_Cooler, GPIO.LOW)
    # Stop PWM
    pwm_Cooler.stop()
    print("\nKeyboard Interrupt: Cooler stopped")

finally:
    print("\nEnd program")