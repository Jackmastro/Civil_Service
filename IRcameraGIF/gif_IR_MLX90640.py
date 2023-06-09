import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import pandas as pd
import numpy as np

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Ask the user to select a file
file_path = filedialog.askopenfilename()  # Prompt the user to select a file

# Load data from the selected file
data = pd.read_csv(file_path)  # Read the selected file

# Convert column to datetime format
data['Time'] = pd.to_datetime(data['Time'], format='%Y_%m_%d_%H_%M_%S')  # Convert 'Time' column to datetime format

# Setup the figure for plotting
fig, ax = plt.subplots(figsize=(12, 7))
therm1 = ax.imshow(np.zeros((24, 32)), vmin=0, vmax=60)  # Create initial plot with zeros
therm1.set_clim(vmin=20, vmax=30)  # Set colorbar limits
cbar = fig.colorbar(therm1)
cbar.set_label('Temperature [$^{\circ}$C]', fontsize=14)
ax.set_xticklabels([])  # Remove x-axis tick labels
ax.set_yticklabels([])  # Remove y-axis tick labels

def update_frame(frame):
    current_data = data.iloc[frame]  # Get the data for the current frame
    temperatures = current_data.drop('Time')  # Exclude the 'Time' column
    temperatures = temperatures.astype(float)
    temperatures = temperatures.values.reshape((24, 32))
    therm1.set_data(np.fliplr(temperatures))  # Update the plot with new temperatures
    plt.title(current_data['Time'])  # Set the plot title to the current timestamp

ani = animation.FuncAnimation(fig, update_frame, frames=len(data), interval=200)  # Create animation

# Extract the file name from the selected path
file_name = os.path.basename(file_path)

# Save animation with a dynamic file name
save_name = 'GIF_IR_' + file_name + '.gif'  # Set the output file name
ani.save(save_name, writer='pillow')  # Save the animation as a GIF