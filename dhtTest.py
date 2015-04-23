#!/usr/bin/python

import time, os, sys
import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTsensor = Adafruit_DHT.DHT22
DHTpin = '22'


humidHigh = 0
humidLow = 100

tempHigh = 0
tempLow = 100

while (True):

	humidity, temperature = Adafruit_DHT.read_retry(DHTsensor, DHTpin)

	if(humidity > humidHigh):
		humidHigh = humidity
	elif(humidity < humidLow):
		humidLow = humidity

	if(temperature > tempHigh):
		tempHigh = temperature
	elif(temperature < tempLow):
		tempLow = temperature
	
	os.system('clear')
	print "------- LIVE READINGS --------"
	print "Humidity: %.1f" % humidity + " %"
	print "Temperature: %.1f" % temperature + " degC"
	print "------------------------------"
	print "      | Temperature | Humidity"
	print "High: | %.1f" % tempHigh + " degC   | %.1f" % humidHigh + " %"
	print "Low:  | %.1f" % tempLow + " degC   | %.1f" % humidLow + " %"
	print "------------------------------"
	
	#  TAKE A LITTLE NAP
	time.sleep(1)