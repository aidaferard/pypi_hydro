#!/usr/bin/env python3

import RPi.GPIO as GPIO
import arduino_data

GPIO.setmode(GPIO.BOARD)

GPIO.setmode(GPIO.BOARD)

# TODO Decide on pH level limit
ph_limit = 7.5
# TODO Decide on Nutrient level
ec_limit = 0
ec_range = 100
# TODO Assign output pin numbers for: Water Pump, Nutrient Pump, pH pump, lights, air pump
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

def check_nutrients(limit):
  """Checks the current nutrient level is in a specified range based on
    the data recieved from the ec sensor
  """
  ec_level = arduino_data.current_ec_level()
  if ec_level - ec_range > limit:
    print('Alert: Nutrients Low - Adding Nutrients and Rechecking')
    add_nutrients()
  elif ec_level + ec_range < limit:
    add_water()
  print('Current Nutrient Level: {}'.format(ec_level))

def add_nutrients():
  """Runs the pump from the nutrient container into the main water reservoir
    for a set amount of time, and then runs the air pump to mix it
    together, then rechecks the nutrient level to ensure it's in the correct range
  """
  GPIO.output(nutrient_pump, GPIO.high)
  time.sleep(20)
  GPIO.output(nutrient_pump, GPIO.low)

  GPIO.output(air_pump, GPIO.high)
  time.sleep(90)
  GPIO.output(air_pump, GPIO.low)

  check_nutrients(ph_limit)

# TODO decide how I want to approach adding water to the system to finish function
def add_water():
  """Needs to either alert user to add water to container or create system to
    automatically add water from either a seperate reservoir or spiget
  """
  print('ADD WATER')