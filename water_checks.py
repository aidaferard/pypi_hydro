#!/usr/bin/env python3

import RPi.GPIO as GPIO
import uno3_data
import time

GPIO.setmode(GPIO.BOARD)

# Recommended pH level 5.5 - 6.5
ph_low = 5.5
ph_high = 6.5
# TODO make these values settable, maybe use ENV variables
# Recommended safe Nutrient level for all plants 1.2 - 1.6
ec_low = 1.2
ec_high = 1.6
# TODO Assign output pin numbers for: Water Pump, Nutrient Pump, pH pump, air pump
water_pump = 1
nutrient_pump = 2
ph_pump = 3
air_pump = 4

GPIO.setup(water_pump, GPIO.OUT)
GPIO.setup(nutrient_pump, GPIO.OUT)
GPIO.setup(ph_pump, GPIO.OUT)
GPIO.setup(air_pump, GPIO.OUT)

def check_ph():
  """Checks the current pH level is lower than the set limit,
    if it's higher, call adjust_ph() to lower ph
  """
  ph_level = uno3_data.current_ph_level()
  if ph_level > ph_high:
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

def check_nutrients():
  """Checks the current nutrient level is in a specified range based on
    the data recieved from the ec sensor
  """
  ec_level = uno3_data.current_ec_level()
  if ec_level < ec_low:
    print('Alert: Nutrients Low - Adding Nutrients and Rechecking')
    add_nutrients()
  elif ec_level > ec_high:
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

  check_nutrients()

# TODO Use Pushbullet to send notification to cell phone
def add_water():
  """Needs to either alert user to add water to container or create system to
    automatically add water from either a seperate reservoir or spiget
  """
  print('ADD WATER')
  time.sleep(300)
  check_nutrients()

  

  