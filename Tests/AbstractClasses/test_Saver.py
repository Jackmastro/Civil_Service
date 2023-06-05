import csv
import datetime

class Saver:
    def __init__(self, time) -> None:
        self.time = time

    def csv_generator(self, file_name=str, data=list) -> None:
        # Create the scv file giving the file name, header, and list data


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
            
        print(f"CSV file '{csv_file}' created successfully.")


    def save_sensors(self, TrHin=None, TrHout=None, TrHamb=None, TrHcool=None, CO2in=None, CO2out=None, NH3in=None, NH3out=None, Flow=None, Scale=None) -> None:
        
        # Check if the sensor are connected

        # Merge data in a single list

        # Update the header

        # if TrHin is not None:


    def save_IR(self, IRcamera=None) -> None:
        if IRcamera is not None:
            #save
        else:
            print(f"{IRcamera.name} not attached.")

    def save_Thermero(self, Thermero=None) -> None:
        if IRcamera is not None:
            #save
        else:
            print(f"{IRcamera.name} not attached.")