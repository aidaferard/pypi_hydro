#!/usr/bin/env python3

import RPi.GPIO as GPIO
import arduino_data

GPIO.setmode(GPIO.BOARD)

GPIO.setmode(GPIO.BOARD)

ph_limit = 7.5
# TODO: Assign output pin numbers for: Water Pump, Nutrient Pump, pH pump, lights, air pump
water_pump = 1
nutrient_pump = 2
ph_pump = 3
air_pump = 4
lights = 5

GPIO.setup(water_pump, GPIO.OUT)
GPIO.setup(nutrient_pump, GPIO.OUT)
GPIO.setup(ph_pump, GPIO.OUT)
GPIO.setup(air_pump, GPIO.OUT)
GPIO.setup(lights, GPIO.OUT)

def check_ph(limit):
    """Checks the current pH level is lower than the set limit,
      if it's higher, call adjust_ph() to lower ph
    """
    ph_level = arduino_data.current_ph_level()
    if ph_level > limit:
        adjust_ph()
    print('Current pH: {}'.format(ph_level))

def adjust_ph():
    """Runs the pump from the pH down container into the main water reservoir
      for a set amount of time, and then runs the air pump to mix it
      together, then rechecks the pH to ensure its in the correct range
    """
    GPIO.output(ph_pump, GPIO.high)
    time.sleep(20)
    GPIO.output(ph_pump, GPIO.low)

    GPIO.output(air_pump, GPIO.high)
    time.sleep(90)
    GPIO.output(air_pump, GPIO.low)

    check_ph(ph_limit)
