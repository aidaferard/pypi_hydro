#!/usr/bin/env python3

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT)

power = 0

def change_relay(power):
    if power > 0:
        GPIO.output(8, GPIO.high)
    else:
        GPIO.output(8, GPIO.low)