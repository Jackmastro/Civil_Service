# matplotlib for Raspberry Pi https://linuxhint.com/install-matplotlib-raspberry-pi/

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation

# Load data
data = pd.read_csv('temperature_data.csv')

# Convert column to data format
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Set up figure
fig, ax = plt.subplots()

# Update function for frames
def update_frame(frame):
    ax.clear()
    
    # Plot the temperature data for the current frame
    current_data = data.iloc[frame]
    temperatures = current_data.drop('timestamp')
    img = ax.imshow(temperatures.values.reshape((24, 32)), cmap='hot', aspect='auto')
    
    # Add a colorbar
    cbar = fig.colorbar(img, ax=ax, fraction=0.046, pad=0.04)
    
    # Format the timestamp on the x-axis
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    
    # Rotate and align the x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Set labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Pixel')
    ax.set_title('MLX90640 Temperature Data')
    
    # Set the timestamp at the bottom
    plt.subplots_adjust(bottom=0.2)
    fig.tight_layout()
    plt.gcf().autofmt_xdate()

# Create animation
ani = animation.FuncAnimation(fig, update_frame, frames=len(data), interval=200)

# Save animation as gif
ani.save('temperature_animation.gif', writer='pillow')