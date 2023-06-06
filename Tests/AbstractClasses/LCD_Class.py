# LCD HD44780 library https://pypi.org/project/RPLCD/ (Documentation: https://rplcd.readthedocs.io/en/latest/index.html)
from RPLCD.i2c import CharLCD

############ MIGLIORAMENTO: USARE ULTIMA ENTRATA DI DATA_TABLE AL POSTO CHE CHIAMARE IL READ_DATA
# oppure prima salvare, poi controller, print

class LCD_HD44780():
    def __init__(self, name=str) -> None:
        self.name = name

        # Set the LCD with i2c
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=20, rows=4)

        print(f"Setup for {self.name} successfully completed.")

    def print_first(self, TrHin=None, TrHout=None, TrHamb=None, CO2in=None, CO2out=None, NH3in=None, NH3out=None) -> None:
        ############TODO ADD COOL AND MOVE CO2 AND NH3
        # Clean the screen
        self.lcd.clear()
        
        # First row
        self.lcd.cursor_pos = (0, 4)
        self.lcd.write_string("T")
        self.lcd.cursor_pos = (0, 8)
        self.lcd.write_string("rH")
        self.lcd.cursor_pos = (0, 12)
        self.lcd.write_string("CO2")
        self.lcd.cursor_pos = (0, 16)
        self.lcd.write_string("NH3")

        # Second row
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("IN")

        if TrHin is not None:
            [Tin_value, rHin_value] = TrHin.read_data()
            self.lcd.cursor_pos = (1, 4)
            self.lcd.write_string(str(int(Tin_value)))
            self.lcd.cursor_pos = (1, 8)
            self.lcd.write_string(str(int(rHin_value)))
        else:
            self.lcd.cursor_pos = (1, 4)
            self.lcd.write_string("-")
            self.lcd.cursor_pos = (1, 8)
            self.lcd.write_string("-")

        if CO2in is not None:
            CO2in_value = CO2in.read_data_point()
            self.lcd.cursor_pos = (1, 12)
            self.lcd.write_string(str(int(CO2in_value)))
        else:
            self.lcd.cursor_pos = (1, 12)
            self.lcd.write_string("-")

        if NH3in is not None:
            NH3in_value = NH3in.read_data_point()
            self.lcd.cursor_pos = (1, 16)
            self.lcd.write_string(str(int(NH3in_value)))
        else:
            self.lcd.cursor_pos = (1, 16)
            self.lcd.write_string("-")

        # Third row
        self.lcd.cursor_pos = (2, 0)
        self.lcd.write_string("OUT")

        if TrHout is not None:
            [Tout_value, rHout_value] = TrHout.read_data()
            self.lcd.cursor_pos = (2, 4)
            self.lcd.write_string(str(int(Tout_value)))
            self.lcd.cursor_pos = (2, 8)
            self.lcd.write_string(str(int(rHout_value)))
        else:
            self.lcd.cursor_pos = (2, 4)
            self.lcd.write_string("-")
            self.lcd.cursor_pos = (2, 8)
            self.lcd.write_string("-")

        if CO2out is not None:
            CO2out_value = CO2out.read_data_point()
            self.lcd.cursor_pos = (2, 12)
            self.lcd.write_string(str(int(CO2out_value)))
        else:
            self.lcd.cursor_pos = (2, 12)
            self.lcd.write_string("-")

        if NH3out is not None:
            NH3out_value = NH3out.read_data_point()
            self.lcd.cursor_pos = (2, 16)
            self.lcd.write_string(str(int(NH3out_value)))
        else:
            self.lcd.cursor_pos = (2, 16)
            self.lcd.write_string("-")

        # Fourth row
        self.lcd.cursor_pos = (3, 0)
        self.lcd.write_string("AMB")

        if TrHamb is not None:
            [Tamb_value, rHamb_value] = TrHamb.read_data()
            self.lcd.cursor_pos = (3, 4)
            self.lcd.write_string(str(int(Tamb_value)))
            self.lcd.cursor_pos = (3, 8)
            self.lcd.write_string(str(int(rHamb_value)))
        else:
            self.lcd.cursor_pos = (3, 4)
            self.lcd.write_string("-")
            self.lcd.cursor_pos = (3, 8)
            self.lcd.write_string("-")

    def print_second(self, Flow=None, IRcamera=None, Thermero=None, Scale=None) -> None:
        #########################TODO aggiungere % del duy cycle
        # Clean the screen
        self.lcd.clear()
        
        # First row
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Flow")

        if Flow is not None:
            flow_value = Flow.read_data_point(type="L/min")
            self.lcd.cursor_pos = (0, 7)
            self.lcd.write_string(str(round(flow_value, 2)))
            self.lcd.cursor_pos = (0, 15)
            self.lcd.write_string("L/min")
        else:
            self.lcd.cursor_pos = (0, 7)
            self.lcd.write_string("-")

        # Second row
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("IRcam")

        if IRcamera is not None:
            IRcam_value = IRcamera.read_data_point()
            self.lcd.cursor_pos = (1, 7)
            self.lcd.write_string(str(int(IRcam_value)))
            self.lcd.cursor_pos = (1, 15)
            self.lcd.write_string("C")
        else:
            self.lcd.cursor_pos = (1, 7)
            self.lcd.write_string("-")

        # Third row
        self.lcd.cursor_pos = (2, 0)
        self.lcd.write_string("Scale")

        if Scale is not None:
            scale_value = Scale.read_data_point()
            self.lcd.cursor_pos = (2, 7)
            self.lcd.write_string(str(round(scale_value/1000, 2)))
            self.lcd.cursor_pos = (2, 15)
            self.lcd.write_string("kg")
        else:
            self.lcd.cursor_pos = (2, 7)
            self.lcd.write_string("-")

        # Fourth row
        self.lcd.cursor_pos = (3, 0)
        self.lcd.write_string("Therm")

        if Thermero is not None:
            Thermero_value = Thermero.read_data_point()
            self.lcd.cursor_pos = (3, 7)
            self.lcd.write_string(str(int(Thermero_value)))
            self.lcd.cursor_pos = (3, 15)
            self.lcd.write_string("C")
        else:
            self.lcd.cursor_pos = (3, 7)
            self.lcd.write_string("-")

    def cleanup(self):
        self.lcd.close(clear=True)

        print(f"Cleanup for {self.name} successfully completed.")