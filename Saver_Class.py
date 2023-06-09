# For data restructuring https://pypi.org/project/pandas/
import pandas as pd
import os

from Sensor_Class import *

class Saver:
    def __init__(self, time_start_process=str) -> None:
        self.name = time_start_process + "_Measurements" # YYMMDD_HHMMSS_Measurements

        print("Setup for saver successfully completed.")
        
    def append_data(self, overview_sensor_dict) -> None:
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

        print(f"CSV file '{file_name}' successfully created.")

    def save_sensor_data(self, RTClock, TrHamb, TrHcool, TrHin, TrHout, CO2in, CO2out, NH3in, NH3out, Flow, Scale) -> None:
        clock_header = ['Time']
        clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)

        data_frames = [clock_data_frame]

        # Append the temperature and relative humidity data_tables
        temperature_humidity_sensors = [(TrHamb, 'Tamb', 'rHamb'), (TrHcool, 'Tcool', 'rHcool'),
                                        (TrHin, 'Tin', 'rHin'), (TrHout, 'Tout', 'rHout')]
        for sensor, temp_header, rh_header in temperature_humidity_sensors:
            if sensor is not None:
                data_frame = pd.DataFrame(sensor.data_table, columns=[temp_header + '[°C]', rh_header + '[%]'])
                data_frames.append(data_frame)
        
        # Append the other data_tables
        other_sensors = [(CO2in, 'CO2in'), (CO2out, 'CO2out'), (NH3in, 'NH3in'),
                         (NH3out, 'NH3out'), (Flow, 'Flow'), (Scale, 'Scale')]
        for sensor, header in other_sensors:
            if sensor is not None:
                data_frame = pd.DataFrame(sensor.data_table, columns=[header + '[{}]'.format(sensor.unit)])
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

    def save_Thermero_data(self, RTClock, thermero) -> None:
        if thermero is not None:
            clock_header = ['Time']
            clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)
            
            thermero_header = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5']
            thermero_data_frame = pd.DataFrame(thermero.data_table, columns=thermero_header)

            # Concatenate data frames and call csv
            data_frame = pd.concat([clock_data_frame, thermero_data_frame], axis=1)
            file_name = self.name + "_Thermero"
            self.generate_csv(data_frame, file_name)
            