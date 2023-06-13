# For data restructuring https://pypi.org/project/pandas/
import pandas as pd
import os

from Sensor_Class import *

class Saver:
    def __init__(self, time_start_process=str) -> None:
        self.name = time_start_process + "_Data" # YY_MM_DD_HH_MM_SS_Data

        print("Setup for saver successfully completed.")
        
    def append_data(self, overview_sensor_dict=dict) -> None:
        # [sensor["sensor"].save_data() for sensor in overview_sensor_dict.values() if sensor["is_connected"] and sensor["sensor"] is not None]
        for sensor in overview_sensor_dict.values():
            if sensor["is_connected"] and sensor["sensor"] is not None:
                sensor["sensor"].save_data()

    def generate_csv(self, data_frame, file_name=str) -> None:
        # Check for the folder path
        folder_path = 'Data'
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name + ".csv")

        # Save the .csv file
        data_frame.to_csv(file_path, index=False)

        print(f"CSV file '{file_name}' successfully created in folder '{folder_path}'.")

    def save_sensor_data(self, overview_sensor_dict=dict) -> None:
        data_frames  =[]

        for sensor_name in overview_sensor_dict.keys():
            if overview_sensor_dict[sensor_name]["is_connected"] and overview_sensor_dict[sensor_name]["sensor"] is not None:
                # Distinguish cases for header of temperature and relative humidity sensors
                if 'TrH' in sensor_name:
                    split_strings = sensor_name.split('TrH', 1)  # Split the string after 'TrH', maximum 1 split
                    temp_header = 'T' + split_strings[1] + '[°C]'
                    rh_header = 'rH' + split_strings[1] + '[%]'
                    header = [temp_header, rh_header]
                else:
                    header = [sensor_name + '[{}]'.format(overview_sensor_dict[sensor_name]["sensor"].unit)]
                
                # Distinguish cases for mean values of IR and Thermero
                if 'IR' in sensor_name or 'Thermero' in sensor_name:
                    data = overview_sensor_dict[sensor_name]["sensor"].data_table_mean
                else:
                    data = overview_sensor_dict[sensor_name]["sensor"].data_table

                data_frame = pd.DataFrame(data, columns=header)
                data_frames.append(data_frame)

            else:
                # Distinguish cases for header of temperature and relative humidity sensors
                if 'TrH' in sensor_name:
                    split_strings = sensor_name.split('TrH', 1)  # Split the string after 'TrH', maximum 1 split
                    temp_header = 'T' + split_strings[1] + '[°C]'
                    rh_header = 'rH' + split_strings[1] + '[%]'
                    header = [temp_header, rh_header]
                else:
                    header = [sensor_name]

                data_frame = pd.DataFrame(columns=header)
                data_frames.append(data_frame)

        # Concatenate data frames
        data_frame = pd.concat(data_frames, axis=1)

        # Call the csv
        file_name = self.name
        self.generate_csv(data_frame, file_name)

    def save_IR_data(self, RTClock, IRcamera) -> None:
        if IRcamera is not None:
            clock_header = ['Time']
            clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)

            IRcamera_header = ['{}[{}]'.format(i+1, IRcamera.unit) for i in range(IRcamera.shape[0] * IRcamera.shape[1])]
            IRcamera_data_frame = pd.DataFrame(IRcamera.data_table, columns=IRcamera_header)

            # Concatenate data frames and call csv
            data_frame = pd.concat([clock_data_frame, IRcamera_data_frame], axis=1)
            file_name = self.name + "_IRcamera"
            self.generate_csv(data_frame, file_name)

    def save_Thermero_data(self, RTClock, Thermero) -> None:
        if Thermero is not None:
            clock_header = ['Time']
            clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)
            
            thermero_header = ['{}{} [{}]'.format(row, col, Thermero.unit) for row in 'ABCD' for col in range(1, 6)]
            thermero_data_frame = pd.DataFrame(Thermero.data_table, columns=thermero_header)

            # Concatenate data frames and call csv
            data_frame = pd.concat([clock_data_frame, thermero_data_frame], axis=1)
            file_name = self.name + "_Thermero"
            self.generate_csv(data_frame, file_name)