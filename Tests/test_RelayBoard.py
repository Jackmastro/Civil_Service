from gpiozero import OutputDevice # More suitable for fans, motors and pumps instead of LED
import time 

# Define pause interval 
t = 5.0

# Define pin locations 
Vent_fans = OutputDevice(24, active_high=False)
Suct_fans = OutputDevice(23, active_high=False)
Cool_fan = OutputDevice(22, active_high=False)

try: 
    while True:
        name = input("What do you want to turn on? (v = ventilation, s = suction, c = cool)\n")
        if name == 'v':
            Vent_fans.on()
            time.sleep(t)
            Vent_fans.off()
        elif name == 's':
            Suct_fans.on()
            time.sleep(t)
            Suct_fans.off()
        elif name == 'c':
            Cool_fan.on()
            time.sleep(t)
            Cool_fan.off()
        else:
            print("Svegliati")

except KeyboardInterrupt:
# Cleanup RPi pins
    Vent_fans.close()
    Suct_fans.close()
    Cool_fan.close()
    
    print("\nYou have successfully terminated the programm.")
    
finally:
# Cleanup RPi pins
    Vent_fans.close()
    Suct_fans.close()
    Cool_fan.close()