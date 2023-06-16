import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Ask the user to select a file
file_path = filedialog.askopenfilename()

# Extract the file name from the selected path
file_name = os.path.basename(file_path)

# File name without the extension
file_name_without_extension = os.path.splitext(file_name)[0]

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

# Ask for the time for the image
valid_time = False
while not valid_time:
    time_image = input("Enter the time for the image (format: YYYY_MM_DD_HH_MM_SS): ")

    try:
        # Convert time_image into datetime object
        time_image = pd.to_datetime(time_image, format='%Y_%m_%d_%H_%M_%S')

        if (data['Time'].iloc[0] <= time_image <= data['Time'].iloc[-1]):
            valid_time = True
        else:
            print("Invalid range! Please enter a time that is between the ranges of time of the file.")

    except ValueError:
        print("Invalid format! Please enter the range in the format: YYYY_MM_DD_HH_MM_SS")

# Find the closest time in the data to the given time_image
closest_time = data['Time'].iloc[(data['Time'] - time_image).abs().argsort()[0]]

# Extract the data for the closest_time
data = data[data['Time'] == closest_time]
print(data)

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

# Update the plot with the final frame
update_frame(0)  # Only a single frame, so use index 0

# Define the save directory path
save_dir = os.path.join(os.getcwd(), '..', 'Images')

# Create the save directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# File name from user
while True:
    save_name_input = input("Type the file name without extension: ")
    save_name = save_name_input.strip() + '.png'
    save_path = os.path.join(save_dir, save_name)

    if not save_name_input:
        print("Empty file name. Please enter a valid file name.")
        continue

    if os.path.exists(save_path):
        overwrite_input = input("File '{}' already exists. Do you want to overwrite it? [y/n] ".format(save_name))
        if overwrite_input.lower() != 'y':
            print("File not overwritten. Please choose a different file name.")
            continue

    try:
        with open(save_path, 'w'):
            pass
    except IOError:
        print("Invalid file name. Please choose a valid file name.")
        continue

    print("File name set to {}.".format(save_name))
    break

# Save animation with a dynamic file name in the specified folder
plt.savefig(save_path)

print(f"File {save_name} correctly saved in {save_dir}.")