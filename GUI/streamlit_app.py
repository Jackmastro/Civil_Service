# pip install streamlit
# In order to run this script you need to type in the terminal: streamlit run "c:/Users/Marco Muttoni/Documents/EAWAG/PALMY/GUI/streamlit_app.py"

import random
import time 
# import setupRPi
import controller
import streamlit as st

# # Run the setup function
# TrH_in, pwm_Heater, pid_Heater = setupRPi()

# System enable 
is_running = False

# Streamlit UI title
st.title("PALMY GUI")

# Streamlite UI start&stop
st.subheader("Start&Stop")
# Create a layout with two columns
start_col, stop_col = st.columns(2)
# Add the start&stop botton to the columns
start_button = start_col.button("Start")
stop_button = stop_col.button("Stop")
# Start and stop functions
if start_button:
    controller.start_control_loop()
if stop_button:
    controller.stop_control_loop()
st.divider()

# # Streamlite UI input values
# st.subheader("User inputs")
# # Create a layout with two columns
# setpoint_col, kp_col, ki_col, kd_col  = st.columns(4)
# # Add input boxes
# setpoint_input = setpoint_col._number_input("Temperature set point")
# kp_input = kp_col._number_input("Kp", value = 0)
# ki_input = ki_col._number_input("Ki", value = 0)
# kd_input = kd_col._number_input("Kd", value = 0)
# # Set inputs functions 
# pid_Heater.set_parameters(kp_input, ki_input, kd_input)
# st.divider()

# Streamlite UI display sensor values
st.subheader("Display temperature values")
# # Create a layout with two columns 
temp_col, rH_col = st.columns(2)
# Add display boxes
temp_col.metric("Temperature", random.random(), "°C") #TrH_in.temperature
rH_col.metric("Humidity", random.random(), "%")#TrH_in.relative_humidity
st.divider()

# Streamlite UI plot sensor values
st.subheader("Plot temperature values")
# Create an empty DataFrame to store sensor data
sensor_data = []
# Add new data point to the DataFrame
sensor_data = sensor_data.append(random.random())
# Plot the sensor data using a line chart
st.line_chart(sensor_data)




