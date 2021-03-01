#!/usr/bin/env python3

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT)

power = 0

def change_relay(relay, power):
    if power > 0:
        GPIO.output(relay, 1)
    else:
        GPIO.output(relay, 0)