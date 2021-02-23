#!/usr/bin/env python3

import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

ph_level = ''
ec_level = ''
i = 0

while True:
    if ser.in_waiting > 0:
        ph_level = ser.readline().decode('utf-8').rstrip()
        ec_level = ser.readline().decode('utf-8').rstrip()
        i += 1
        if i == 60:
            # TODO: Record data in a csv file every hour
            i = 0

def current_ph_level():
    return int(ph_level)

def current_ec_level():
    return ec_level