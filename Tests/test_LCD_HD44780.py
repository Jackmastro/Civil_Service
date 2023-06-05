# LCD HD44780 library https://pypi.org/project/RPLCD/ (Documentation: https://rplcd.readthedocs.io/en/latest/index.html)
from RPLCD.i2c import CharLCD
import time

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=20, rows=4)

try:
    number = 3
    lcd.cursor_pos = (0, 1)
    lcd.write_string(str(number))
    lcd.cursor_pos = (3, 0)
    lcd.write_string("01234567890123456789")
    time.sleep(10.0)
    lcd.close(clear=True)
    
except KeyboardInterrupt:
    lcd.close(clear=True)
    print("You have successfully interrupted the programm.")
    
finally:
    lcd.close(clear=True)
