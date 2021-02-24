#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# TODO set pin numbers, maybe use ENV variables
water_pump = 1
nutrient_pump = 2
ph_pump = 3
air_pump = 4

GPIO.setup(water_pump, GPIO.OUT)
GPIO.setup(nutrient_pump, GPIO.OUT)
GPIO.setup(ph_pump, GPIO.OUT)
GPIO.setup(air_pump, GPIO.OUT)

def drip_on():
  """Turns on the water pump to run the drip irrigation for
    the system, also turns on the air pump to help ensure good
    oxygen levels in the water
  """
  if GPIO.input(ph_pump) and GPIO.input(nutrient_pump):
    # Wait if nutrients or ph being added
    time.sleep(300)
    drip_on()
  GPIO.output(water_pump, GPIO.high)
  GPIO.output(air_pump, GPIO.high)
  time.sleep(600)
  GPIO.output(water_pump, GPIO.low)
  GPIO.output(air_pump, GPIO.low)

