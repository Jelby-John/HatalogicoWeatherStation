#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time, os, sys
from random import randint

# Initialise the PWM device using the default address
pwm = PWM(0x70)
pwm.setPWMFreq(100)

brightRed = 3
brightGreen = 5
humidRed = 7
humidGreen = 9
tempRed = 11
tempGreen = 13

pwm.setPWM(brightRed, 0, 0)
pwm.setPWM(brightGreen, 0, 4095)
pwm.setPWM(humidRed, 0, 0)
pwm.setPWM(humidGreen, 0, 4095)
pwm.setPWM(tempRed, 0, 0)
pwm.setPWM(tempGreen, 0, 4095)
time.sleep(3)

pwm.setPWM(brightRed, 0, 4095)
pwm.setPWM(brightGreen, 0, 0)
pwm.setPWM(humidRed, 0, 4095)
pwm.setPWM(humidGreen, 0, 0)
pwm.setPWM(tempRed, 0, 4095)
pwm.setPWM(tempGreen, 0, 0)
time.sleep(1)

pwm.setPWM(brightRed, 0, 0)
pwm.setPWM(humidRed, 0, 0)
pwm.setPWM(tempRed, 0, 0)

for brightness in range(4095, 0, 16):
	pwm.setPWM(brightRed, 0, brightness)
	pwm.setPWM(humidRed, 0, brightness)
	pwm.setPWM(tempRed, 0, brightness)

for brightness in range(0, 4095, 8):
	pwm.setPWM(brightGreen, 0, brightness)
	pwm.setPWM(humidGreen, 0, brightness)
	pwm.setPWM(tempGreen, 0, brightness)
	pwm.setPWM(brightRed, 0, brightness)
	pwm.setPWM(humidRed, 0, brightness)
	pwm.setPWM(tempRed, 0, brightness)

while (True):
	randRed = randint(1024,4095)
	randGreen = randint(1024,4095)

	pwm.setPWM(brightGreen, 0, randGreen)
	pwm.setPWM(humidGreen, 0, randGreen)
	pwm.setPWM(tempGreen, 0, randGreen)
	pwm.setPWM(brightRed, 0, randRed)
	pwm.setPWM(humidRed, 0, randRed)
	pwm.setPWM(tempRed, 0, randRed)
	time.sleep(5)