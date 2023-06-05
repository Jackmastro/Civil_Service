import time
import board
import adafruit_ahtx0
import csv
                            
# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Define AM2315 sensors connected to channels of the multiplexer
TrH_try = adafruit_ahtx0.AHTx0(i2c)

# Create list to store and paste sensor values in a csv file 
data = []

try: 
    while True:
        # Read humidity and t emperature vales from sensors. It returns a tuple, an unchangeable list of values.
        T = TrH_try.temperature
        rH = TrH_try.relative_humidity
        print(T)
        print(rH)

        # Append data to list
        data.append({'sensor_id': 'T&rH try', 'temperature': T, 'humidity': rH, 'time': time.time})
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nKeyboard Interrupt: Saving data in a csv file")

    # Define the fieldnames for the CSV file
    fieldnames = ['sensor_id', 'temperature', 'humidity', 'time']

    # Write the data to a CSV file
    csvfilename = input("CSV filename? (Do not forget .csv babbuino)")
    with open(csvfilename, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames) # DictWriter is a class in Python's built-in csv module that allows writing dictionaries to CSV files. It works similar to the csv.writer class but instead of taking a list of values, it takes a dictionary where each key represents a column header and the corresponding value is the data to be written in that column.
        writer.writeheader() # Writes the headers to the CSV file
        for row in data:
            writer.writerow(row) # Writes a row of values to the CSV file based on the keys of the dictionary and ensures that each value is placed under the corresponding header specified in the fieldnames parameter.
    
    print("You have successfully terminated the programm.")