#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
from Adafruit_ADS1x15 import ADS1x15
import time, os, sys
import Adafruit_DHT

# HOW MANY CYCLES TO BE PERFORMED BEFORE SHOWING THE HIGH AND LOW SEQUENCE
# SET TO 0 FOR OFF
intervalHighLow = 60
# HOW LONG TO REST BETWEEN CYCLES - ZERO IS FINE
intervalSleep = 1
# HOW LONG TO DISPLAY THE HIGH AND LOW DISPLAYS
intervalDisplay = 5
# INTERVAL COUNTER/TRACKER. ALWAYS START AT 1
intervalCounter = 1

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTsensor = Adafruit_DHT.DHT22
DHTpin = '22'

# SETUP THE PWMS
pwm = PWM(0x70)
pwm.setPWMFreq(100)

# SETUP THE ADCS
ADS1015 = 0x00
gain = 6144
sps = 100
adc = ADS1x15(address=0x49, ic=ADS1015)

# SET LEFT AND RIGHT POSITION FOR SERVOS
servoMin = 380
servoMax = 1150

# DEFINE SERVO PINS ON HATALOGICO PWMS
servoLight = 8
servoHumid = 10
servoTemp = 12

# DEFINE MAX AND MIN VALUES
tempMin = 40
tempMax = 15
humidMin = 100
humidMax = 0
lightMin = 1
lightMax = 2800

# DECLARE DEFAULT VALUES FOR HIGH AND LOW TRACKERS
tempHigh = 0
tempLow = 100
humidHigh = 0
humidLow = 100
lightHigh = 0
lightLow = 100

# LED PIN CONFIG ON HATALOGICO PWMS
brightRed = 3
brightGreen = 5
humidRed = 7
humidGreen = 9
tempRed = 11
tempGreen = 13

def showHighs():
	# SCALE READINGS INTO OUTPUT VALUES
	tempPercent = (tempHigh - tempMin) / (tempMax - tempMin)
	tempOutput = int(tempPercent * (servoMax - servoMin) + servoMin)

	lightPercent = (lightHigh - lightMin) / (lightMax - lightMin)
	lightOutput = int(lightPercent * (servoMax - servoMin) + servoMin)

	humidPercent = (humidHigh - humidMin) / (humidMax - humidMin)
	humidOutput = int(humidPercent * (servoMax - servoMin) + servoMin)

	pwm.setPWM(brightGreen, 0, 4095)
	pwm.setPWM(brightRed, 0, 0)
	pwm.setPWM(humidGreen, 0, 4095)
	pwm.setPWM(humidRed, 0, 0)
	pwm.setPWM(tempGreen, 0, 4095)
	pwm.setPWM(tempRed, 0, 0)

	pwm.setPWM(servoTemp, 0, tempOutput)
	pwm.setPWM(servoHumid, 0, humidOutput)
	pwm.setPWM(servoLight, 0, lightOutput)

	time.sleep(intervalDisplay)

def showLows():
	# SCALE READINGS INTO OUTPUT VALUES
	tempPercent = (tempLow - tempMin) / (tempMax - tempMin)
	tempOutput = int(tempPercent * (servoMax - servoMin) + servoMin)

	lightPercent = (lightLow - lightMin) / (lightMax - lightMin)
	lightOutput = int(lightPercent * (servoMax - servoMin) + servoMin)

	humidPercent = (humidLow - humidMin) / (humidMax - humidMin)
	humidOutput = int(humidPercent * (servoMax - servoMin) + servoMin)

	pwm.setPWM(brightGreen, 0, 0)
	pwm.setPWM(brightRed, 0, 4095)
	pwm.setPWM(humidGreen, 0, 0)
	pwm.setPWM(humidRed, 0, 4095)
	pwm.setPWM(tempGreen, 0, 0)
	pwm.setPWM(tempRed, 0, 4095)

	pwm.setPWM(servoTemp, 0, tempOutput)
	pwm.setPWM(servoHumid, 0, humidOutput)
	pwm.setPWM(servoLight, 0, lightOutput)

	time.sleep(intervalDisplay)

def lightsOff():
	pwm.setPWM(brightRed, 0, 4095)
	pwm.setPWM(humidRed, 0, 4095)
	pwm.setPWM(tempRed, 0, 4095)
	pwm.setPWM(brightGreen, 0, 4095)
	pwm.setPWM(humidGreen, 0, 4095)
	pwm.setPWM(tempGreen, 0, 4095)

def startup():
	lightsOff()
	# TURN ON RED LEDS FOR SERVO START-UP PROCEDURE
	pwm.setPWM(brightRed, 0, 0)
	pwm.setPWM(humidRed, 0, 0)
	pwm.setPWM(tempRed, 0, 0)
	
	time.sleep(3)
	lightsOff()

	pwm.setPWM(brightGreen, 0, 0)
	pwm.setPWM(humidGreen, 0, 0)
	pwm.setPWM(tempGreen, 0, 0)

	time.sleep(5)
	lightsOff()


startup()
while (True):
	if(intervalCounter == intervalHighLow):
		showHighs()
		showLows()
		lightsOff()
		
		intervalCounter = 1

	elif(intervalCounter < intervalHighLow):
		intervalCounter += 1

		# GET HUMIDITY AND TEMPERATURE READINGS FROM DHT22
		humidity, temperature = Adafruit_DHT.read_retry(DHTsensor, DHTpin)

		ldrValue = adc.readADCSingleEnded(0, gain, sps)
		lightValue = (ldrValue - lightMin) / (lightMax - lightMin) * 100

		# SCALE READINGS INTO OUTPUT VALUES
		tempPercent = (temperature - tempMin) / (tempMax - tempMin)
		tempOutput = int(tempPercent * (servoMax - servoMin) + servoMin)

		humidPercent = (humidity - humidMin) / (humidMax - humidMin)
		humidOutput = int(humidPercent * (servoMax - servoMin) + servoMin)

		lightPercent = lightValue / 100
		lightOutput = int(lightPercent * (servoMax - servoMin) + servoMin)
		
		# CHECK FOR HIGH AND LOW VALUES
		# HUMIDITY
		if(humidity > humidHigh):
			humidHigh = humidity
		if(humidity < humidLow):
			humidLow = humidity	

		# TEMPERATURE
		if(temperature > tempHigh):
			tempHigh = temperature
		if(temperature < tempLow):
			tempLow = temperature	

		# BRIGHTNESS
		if(lightValue > lightHigh):
			lightHigh = lightValue
		if(lightValue < lightLow):
			lightLow = lightValue

		os.system('clear')

		print "----- INPUTS ------"
		print "Temperature: %d" % temperature
		print "Humidity: %d" % humidity
		print "Brightness: %d" % lightValue

		print "----- OUTPUTS -----"
		print "Temperature: %d" % tempOutput
		print "Humidity: %d" % humidOutput
		print "Brightness: %d" % lightOutput

		print "----- HISTORY -----"
		print "      | Temperature | Humidity | Brightness   "
		print "High: | %.1f" % tempHigh + " degC   | %.1f" % humidHigh + " %%   | %.1f" % lightHigh + " %"
		print "Low:  | %.1f" % tempLow + " degC   | %.1f" % humidLow + " %%   | %.1f" % lightLow + " %"
		print "------------------------------"

		pwm.setPWM(servoTemp, 0, tempOutput)
		pwm.setPWM(servoHumid, 0, humidOutput)
		pwm.setPWM(servoLight, 0, lightOutput)

		time.sleep(intervalSleep)	
