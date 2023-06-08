# RTC Real Time Clock DS1307 library https://docs.circuitpython.org/projects/ds1307/en/latest/index.html

import time
import board
import adafruit_ds1307

i2c = board.I2C()
rtc = adafruit_ds1307.DS1307(i2c)

# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# pylint: disable-msg=using-constant-test
if False:  # change to True if you want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023, 6, 8, 16, 26, 30, 3, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
# pylint: enable-msg=using-constant-test

# Main loop:
while True:
    t = rtc.datetime
    print("{}_{}_{}_{}_{}_{:01}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    print(time.time())
#     print(t)     # uncomment for debugging
#     print(
#         "The date is {} {}/{}/{}".format(
#             days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
#         )
#     )
#     print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(1)  # wait a second