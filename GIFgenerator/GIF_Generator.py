import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Ask the user to select a file
file_path = filedialog.askopenfilename()

# Extract the file name from the selected path
file_name = os.path.basename(file_path)

# Distinguish between IR camera or Thermero
if 'IR' in file_name:
    shape = (24, 32)
elif 'Thermero' in file_name:
    shape = (5, 4)
else:
    raise ValueError('file_name has to include "IR" or "Thermero". Received: {}'.format(file_name))

# Load data from the selected file
data = pd.read_csv(file_path)

# Convert column to datetime format
data['Time'] = pd.to_datetime(data['Time'], format='%Y_%m_%d_%H_%M_%S')

# Ask for lower and higher ranges
valid_range = False
while not valid_range:
    lower_range = input("Enter the lower range (format: YYYY-MM-DD HH:MM:SS): ")
    upper_range = input("Enter the higher range (format: YYYY-MM-DD HH:MM:SS): ")

    try:
        # Convert ranges into datetime objects
        lower_range = pd.to_datetime(lower_range)
        upper_range = pd.to_datetime(upper_range)

        if lower_range <= upper_range:
            valid_range = True
        else:
            print("Invalid range! Please enter a lower range that is less than or equal to the higher range.")

        if (data['Time'].iloc[0] <= lower_range <= data['Time'].iloc[-1]):
            valid_time = True
        else:
            print("Invalid range! Please enter a lower range that is between the ranges of time of the file.")
        
        if (data['Time'].iloc[0] <= upper_range <= data['Time'].iloc[-1]):
            valid_time = True
        else:
            print("Invalid range! Please enter a upper range that is between the ranges of time of the file.")

    except ValueError:
        print("Invalid format! Please enter the range in the format: YYYY-MM-DD HH:MM:SS")

# Cut the data within the specified range
data = data.loc[(data['Time'] >= lower_range) & (data['Time'] <= upper_range)]

# Setup the figure for plotting
fig, ax = plt.subplots(figsize=(12, 7))

# Create initial plot with zeros
plot = ax.imshow(np.zeros(shape), vmin=0, vmax=50, cmap='hot')
plot.set_clim(vmin=15, vmax=50)  # Set colorbar limits
cbar = fig.colorbar(plot)
cbar.set_label('Temperature [°C]', fontsize=14)
ax.set_xticklabels([])  # Remove x-axis tick labels
ax.set_yticklabels([])  # Remove y-axis tick labels
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks

def update_frame(frame):
    current_data = data.iloc[frame]  # Get the data for the current frame
    temperatures = current_data.drop('Time')  # Exclude the 'Time' column
    temperatures = temperatures.astype(float)
    temperatures = temperatures.values.reshape(shape)
    plot.set_data(np.fliplr(temperatures))  # Update the plot with new temperatures
    plt.title(current_data['Time'])  # Set the plot title to the current timestamp

# Create animation
ani = animation.FuncAnimation(fig, update_frame, frames=len(data), interval=200)

# Save animation with a dynamic file name
save_name = file_name + '_GIF.gif'  # Set the output file name
# remove .csv expansion
ani.save(save_name, writer='pillow')  # Save the animation as a GIF
# save in the GIF data