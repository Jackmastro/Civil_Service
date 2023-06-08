import pandas as pd
import time
import os

from Sensor_Class import *

class Saver:
    def __init__(self, time_start_process=str) -> None:
        self.name = time_start_process + "_Measurements" # YYMMDD_HHMMSS_Measurements

        print("Setup for saver successfully completed.")

    def generate_csv(self, file_name=str, data_frame=None) -> None:
        # Create the csv file giving the file name, header, and list data

        folder_path = '../Data'
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name + ".csv")

        data_frame.to_csv(file_path, index=False)

        print(f"CSV file '{file_name}' successfully created.")

    def save_sensor_data(self, RTClock=None, TrHamb=None, TrHcool=None, TrHin=None, TrHout=None, CO2in=None, CO2out=None, NH3in=None, NH3out=None, Flow=None, Scale=None) -> None:
        clock_header = ['Time']
        clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)

        data_frames = [clock_data_frame]

        sensor_list = [TrHamb, TrHcool, TrHin, TrHout, CO2in, CO2out, NH3in, NH3out, Flow, Scale]
        header_list = ['Tamb', 'rHamb', 'Tcool', 'rHcool', 'Tin', 'rHin', 'Tout', 'rHout', 'CO2in', 'CO2out', 'NH3in', 'NH3out', 'Flow', 'Scale']

        for sensor, header in zip(sensor_list, header_list):
            if sensor is not None:
                data_frame = pd.DataFrame(sensor.data_table, columns=[header])
                data_frames.append(data_frame)
            else:
                print(f"{sensor.name} not connected.")

        # Concatenate data frames
        data_frame = pd.concat(data_frames, axis=1)

        # Call the csv
        file_name = self.name
        self.generate_csv(file_name, data_frame)

    def save_IR_data(self, RTClock=None, IRcamera=None) -> None:
        if IRcamera is not None:
            clock_header = ['Time']
            clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)

            IRcamera_header = ['' for _ in range(IRcamera.shape[0] * IRcamera.shape[1])]
            IRcamera_data_frame = pd.DataFrame(IRcamera.data_table, columns=IRcamera_header)

            # Concatenate data frames and call csv
            data_frame = pd.concat([clock_data_frame, IRcamera_data_frame], axis=1)
            file_name = self.name + "_IRcamera"
            self.generate_csv(file_name, data_frame)
        else:
            print(f"{IRcamera.name} not connected.")

    def save_Thermero_data(self, RTClock=None, Thermero=None) -> None:
        if Thermero is not None:
            clock_header = ['Time']
            clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)
            
            thermero_header = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5']
            thermero_data_frame = pd.DataFrame(Thermero.data_table, columns=thermero_header)

            # Concatenate data frames and call csv
            data_frame = pd.concat([clock_data_frame, thermero_data_frame], axis=1)
            file_name = self.name + "_Thermero"
            self.generate_csv(file_name, data_frame)
        else:
            print(f"{Thermero.name} not connected.")

################################
time_experiment = time.struct_time((2023, 6, 5, 15, 14, 15, 0, -1, -1)) # update da RTC
saver = Saver(time_experiment)