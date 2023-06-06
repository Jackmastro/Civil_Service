import csv
import time
import datetime

from Sensor_Class import *

class Saver:
    def __init__(self, time_start_process=str) -> None:
        self.name = time_start_process + "_Measurements" # YYMMDD_HHMMSS_Measurements

    def csv_generator(self, file_name=str, header=list, data=list) -> None:
        # Create the csv file giving the file name, header, and list data

        print(f"CSV file '{file_name}' successfully created.")

    def save_sensors(self, TrHin=None, TrHout=None, TrHamb=None, TrHcool=None, CO2in=None, CO2out=None, NH3in=None, NH3out=None, Flow=None, Scale=None) -> None:
        
        # Check if the sensor are connected
        if Scale is not None:
            print("connected")

        # Merge data in a single list

        # Update the header and keep only one time stamp

        ###########TODO CHANGE ALL DATA_TABLE WITH TIME STAMP AS IN THE FIRST COLUMN


    def save_IR(self, IRcamera=None) -> None:
        IR_file_name = self.name + "_IRcamera"
        IR_header = ['Time']

        if IRcamera is not None:
            IR_data = IRcamera.data_table()
            #### INSERT FIRST COLUMN FROM MAIN
            self.csv_generator(IR_file_name, IR_header, IR_data)
        else:
            print(f"{IRcamera.name} not attached.")

    def save_Thermero(self, Thermero=None) -> None:
        Thermero_file_name = self.name + "_Thermero"
        Thermero_header = ['Time', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5']

        if Thermero is not None:
            Thermero_data = Thermero.data_table()
            ###### INSERT FIRST COLUMN FROM MAIN
            self.csv_generator(Thermero_file_name, Thermero_header, Thermero_data)
        else:
            print(f"{Thermero.name} not attached.")

#########################
# Get the current timestamp from the RTC clock
current_timestamp = datetime.datetime.now()

# Example temperature data as a list
temperature_data = [25.5, 26.3, 24.8, 23.9, 25.1, 24.7, 26.0, 26.8, 25.2, 24.5, 23.7, 24.9, 26.1, 25.9, 25.6, 24.3, 23.8, 24.6, 26.2, 25.4]

# Create a list of rows for the CSV file
rows = [[current_timestamp] + temperature_data]

# Specify the CSV file path
csv_file = 'temperature_data.csv'

# Write the data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Timestamp'] + [f'Temperature {i}' for i in range(1, 21)])
    
    # Write the data rows
    writer.writerows(rows)

###############
time_experiment = time.struct_time((2023, 6, 5, 15, 14, 15, 0, -1, -1)) # update da RTC
saver = Saver(time_experiment)