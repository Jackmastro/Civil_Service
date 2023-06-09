# RTC Real Time Clock DS1307 library https://docs.circuitpython.org/projects/ds1307/en/latest/index.html

import time
import board
import adafruit_ds1307

i2c = board.I2C()
rtc = adafruit_ds1307.DS1307(i2c)

# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

#                     year, mon, date, hour, min, sec, wday, yday, isdst
t = time.struct_time((2023, 6, 8, 16, 26, 30, 3, -1, -1))
# you must set year, mon, date, hour, min, sec and weekday
# yearday is not supported, isdst can be set but we don't do anything with it at this time
print("Setting time to:", t)  # uncomment for debugging
rtc.datetime = t

while True:
    t = rtc.datetime
    print("{}_{}_{}_{}_{}_{}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    print(time.time())
    time.sleep(1)  # wait a second