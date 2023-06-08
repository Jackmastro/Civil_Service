import pandas as pd
import time

from Sensor_Class import *

class Saver:
    def __init__(self, time_start_process=str) -> None:
        self.name = time_start_process + "_Measurements" # YYMMDD_HHMMSS_Measurements

        print("Setup for saver successfully completed.")

    def csv_generator(self, file_name=str, data_frame=None) -> None:
        # Create the csv file giving the file name, header, and list data

        file_path = file_name + ".csv"

        data_frame.to_csv(file_path, index=False)

        print(f"CSV file '{file_name}' successfully created.")

    def save_sensors(self, RTClock=None, TrHamb=None, TrHcool=None, TrHin=None, TrHout=None, CO2in=None, CO2out=None, NH3in=None, NH3out=None, Flow=None, Scale=None) -> None:
        clock_header = ['Time']
        clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)

        TrHamb_header = ['Tamb', 'rHamb']
        TrHamb_data_frame = pd.DataFrame(TrHamb.data_table, columns=TrHamb_header)

        TrHcool_header = ['Tcool', 'rHcool']
        TrHcool_data_frame = pd.DataFrame(TrHcool.data_table, columns=TrHcool_header)

        TrHin_header = ['Tin', 'rHin']
        TrHin_data_frame = pd.DataFrame(TrHin.data_table, columns=TrHin_header)

        TrHout_header = ['Tout', 'rHout']
        TrHout_data_frame = pd.DataFrame(TrHout.data_table, columns=TrHout_header)

        CO2in_header = ['CO2in']
        CO2in_data_frame = pd.DataFrame(CO2in.data_table, columns=CO2in_header)

        CO2out_header = ['CO2out']
        CO2out_data_frame = pd.DataFrame(CO2out.data_table, columns=CO2out_header)

        NH3in_header = ['NH3in']
        NH3in_data_frame = pd.DataFrame(NH3in.data_table, columns=NH3in_header)

        NH3out_header = ['NH3out']
        NH3out_data_frame = pd.DataFrame(NH3out.data_table, columns=NH3out_header)

        flow_header = ['Flow']
        flow_data_frame = pd.DataFrame(Flow.data_table, columns=flow_header)

        # Concatenate data frames
        data_frame = pd.concat([clock_data_frame, TrHamb_data_frame, TrHcool_data_frame, TrHin_data_frame, TrHout_data_frame, CO2in_data_frame, CO2out_data_frame, NH3in_data_frame, NH3out_data_frame, flow_data_frame], axis=1)

        if Scale is not None:
            scale_header = ['Scale']
            scale_data_frame = pd.DataFrame(Scale.data_table, columns=scale_header)
            
            data_frame = pd.concat([data_frame, scale_data_frame], axis=1)
        else:
            print(f"{Scale.name} not connected.")
        
        # Call the csv
        file_name = self.name
        self.csv_generator(file_name, data_frame)

    def save_IRcamera(self, RTClock=None, IRcamera=None) -> None:
        if IRcamera is not None:
            clock_header = ['Time']
            clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)

            IRcamera_header = ['' for _ in range(IRcamera.shape[0] * IRcamera.shape[1])]
            IRcamera_data_frame = pd.DataFrame(IRcamera.data_table, columns=IRcamera_header)

            # Concatenate data frames and call csv
            data_frame = pd.concat([clock_data_frame, IRcamera_data_frame], axis=1)
            file_name = self.name + "_IRcamera"
            self.csv_generator(file_name, data_frame)
        else:
            print(f"{IRcamera.name} not connected.")

    def save_Thermero(self, RTClock=None, Thermero=None) -> None:
        if Thermero is not None:
            clock_header = ['Time']
            clock_data_frame = pd.DataFrame(RTClock.data_table, columns=clock_header)
            
            thermero_header = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5']
            thermero_data_frame = pd.DataFrame(Thermero.data_table, columns=thermero_header)

            # Concatenate data frames and call csv
            data_frame = pd.concat([clock_data_frame, thermero_data_frame], axis=1)
            file_name = self.name + "_Thermero"
            self.csv_generator(file_name, data_frame)
        else:
            print(f"{Thermero.name} not connected.")

################################
time_experiment = time.struct_time((2023, 6, 5, 15, 14, 15, 0, -1, -1)) # update da RTC
saver = Saver(time_experiment)