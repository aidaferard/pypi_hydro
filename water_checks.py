#!/usr/bin/env python3

import RPi.GPIO as GPIO
import uno3_data
import time
import json
import alerts

GPIO.setmode(GPIO.BOARD)

# Recommended pH level 5.5 - 6.5
ph_low = 5.5
ph_high = 6.5
# TODO make these values settable, set up json file to store data and different plant profiles
# Recommended safe Nutrient level for all plants 1.2 - 1.6
ec_low = 1.2
ec_high = 1.6
# TODO Assign output pin numbers for: Water Pump, Nutrient Pump, pH pump, air pump
water_pump = 1
nutrient_pump = 2
ph_pump = 3
air_pump = 4
water_scale = 5
nutrient_scale = 6
ph_scale = 7

GPIO.setup(water_pump, GPIO.OUT)
GPIO.setup(nutrient_pump, GPIO.OUT)
GPIO.setup(ph_pump, GPIO.OUT)
GPIO.setup(air_pump, GPIO.OUT)

GPIO.setup(water_scale, GPIO.IN)
GPIO.setup(nutrient_scale, GPIO.IN)
GPIO.setup(ph_scale, GPIO.IN)

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

  check_ph()

def check_nutrients():
  """Checks the current nutrient level is in a specified range based on
    the data recieved from the ec sensor
  """
  ec_level = uno3_data.current_ec_level()
  if ec_level < ec_low:
    print('Alert: Nutrients Low - Adding Nutrients and Rechecking')
    add_nutrients()
  elif ec_level > ec_high:
    dilute_nutrients(ec_level, ec_high)
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
def dilute_nutrients(nutrient_level, nutrient_high):
  """Needs to either alert user to add water to container or create system to
    automatically add water from either a seperate reservoir or spiget
  """
  alerts.send_alert('dilute-nutrients', nutrient_level)

def check_liquid_levels():
  """Reads the sensor data from the scales attached to the Pi's GPIO ports
    then reads the weight of just the liquid of each when its full and the weight
    of the container when its empty from a JSON file created by the 
    set_liquid_weights() function
  """
  water_weight = GPIO.input(water_scale)
  nutrient_weight = GPIO.input(nutrient_scale)
  ph_weight = GPIO.input(ph_scale)

  with open('<path to json file>') as weights_chart:
    weights = json.load(weights_chart)
  
  ph_full_weight = weights['ph']['liquid_wieght']
  ph_empty_weight = weights['ph']['empty_weight']
  nutrient_full_weight = weights['nutrient']['liqiud_weight']
  nutrient_empty_weight = weights['nutrient']['empty_weight']
  water_full_weight = weights['water']['liquid_weight']
  water_empty_weight = weights['water']['empty_weight']

  ph_percentage = int(((ph_weight - ph_empty_weight) / ph_full_weight) * 100)
  nutrient_percentage = int(((nutrient_weight - nutrient_empty_weight) / nutrient_full_weight) * 100)
  water_percentage = int(((water_weight - water_empty_weight) / water_full_weight) * 100)

  # TODO Decide on percentages for alerting, should probably be editable and saved in the
  # JSON as well so they can be updated as we learn or the computer learns
  if water_percentage < 50:
    alerts.send_alert('water-level', water_percentage)
  if nutrient_percentage < 50:
    alerts.send_alert('nutrient-level', water_percentage)
  if ph_percentage < 50:
    alerts.send_alert('ph-level', water_percentage)
  

  return water_percentage, nutrient_percentage, ph_percentage

def set_liquid_weights(liquid, empty_weight, full_weight, volume):
  """Takes the values set by the user using the scale to measure each container
    before and after it's been filled and user inputed # of liters of liquid
    to calculate the liquid weight then updates the json file with the new weights
  """
  liquid_weight = full_weight - empty_weight
  # TODO use liter_weight to calculate usage/day week and learn to predict future needs
  liter_weight = liquid_weight / volume

  # TODO create a json file with default values
  with open('config/liquid_weights.json', 'w+') as weights:
    json_weights = json.load(weights)
    json_weights[liquid]['empty_weight'] = empty_weight
    json_weights[liquid]['full_weight'] = full_weight
    json_weights[liquid]['liquid_weight'] = liquid_weight
    json_weights[liquid]['liter_weight'] = liter_weight
    json.dump(json_weights, weights)

def set_solution_levels(profile, ph_low, ph_high, ec_low, ec_high):
  """Gathers data passed from the user interface and saves it to a json file to be
    referenced later, also saving it under a profile name so it can be used again later
    if it's a good setting
  """
  # TODO create a default json file with default values to start program
  with open('config/solution_profiles.json', 'w+') as solution_profiles:
    profiles = json.load(solution_profiles)
    profiles[profile]['ph_low'] = ph_low
    profiles[profile]['ph_high'] = ph_high
    profiles[profile]['ec_low'] = ec_low
    profiles[profile]['ec_high'] = ec_high
    json.dump(profiles, solution_profiles)


