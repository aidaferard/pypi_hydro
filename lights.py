#!/usr/bin/env python3

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# TODO set pin numbers, maybe use ENV variables
lights = 1

GPIO.setup(lights, GPIO.OUT)

if GPIO.input():
  lights_off()
else:
  lights_on()

def lights_on():
  """Turns the lights on

    TODO add a var and split lights to adjust for certain plants only
  """
  GPIO.output(lights, GPIO.high)

def lights_off()
  """Turns the lights off
  """
  GPIO.output(lights, GPIO.low)
