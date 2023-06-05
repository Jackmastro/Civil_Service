import time
import threading
import streamlit as st

def control_loop(pid_Heater, TrH_in, pwm_Heater):
    global is_running
    is_running = True
    while is_running:
        # Get and apply actuator PID computed duty cycle 
        pwm_output = pid_Heater.GetActuatorOutput(TrH_in.temperature)
        pwm_Heater.ChangeDutyCycle(pwm_output)
        # Wait time
        time.sleep(1.0)

def stop_control_loop(pwm_Heater):
    global is_running
    is_running = False
    # Stop PWM
    pwm_Heater.stop()
    st.write("Control loop stopped.")

def start_control_loop(pid_Heater, TrH_in, pwm_Heater):
    global is_running
    if not is_running:
        # Start a new thread for the control loop
        threading.Thread(target=control_loop, args=(pid_Heater, TrH_in, pwm_Heater)).start() # By running the control loop in a separate thread, you prevent it from blocking the main thread, ensuring that your Streamlit app remains responsive.
        st.write("Control loop started.")
    else:
        st.write("Control loop is already running.")