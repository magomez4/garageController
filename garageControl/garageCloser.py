import sys
import time
import RPi.GPIO as GPIO
from datetime import datetime

#sys.stdout = open('/home/pi/Desktop/garageControl/loggerGarage.txt', 'w')
myfile = open('/home/pi/Desktop/garageControl/loggerGarage.txt', 'a')
currentTime = datetime.now()
myfile.write(f'Started garage controller date: {currentTime}\n')
myfile.close()

doorOpen = GPIO.HIGH
doorClosed = GPIO.LOW

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup() #start with a clean setup

class RelayController:
	signalPin = 0
	def __init__(self, sigPin):
		self.signalPin = sigPin
		GPIO.setup(self.signalPin, GPIO.OUT)
		
	def closeRelay(self):
		if GPIO.input(self.signalPin):
			#print("Relay is closed")
			print(" ")
		else:
			GPIO.output(self.signalPin, GPIO.HIGH)
	
	def openRelay(self):
		GPIO.output(self.signalPin, GPIO.LOW)
		
	def closeAndOpen(self):
		GPIO.output(self.signalPin, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(self.signalPin, GPIO.LOW)

class DoorSensor:
	signalPin = 0
	def __init__(self, sigPin):
		self.signalPin = sigPin
		GPIO.setup(self.signalPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		
	def readSensor(self):
		return GPIO.input(self.signalPin)

relay = RelayController(23)
doorSensor = DoorSensor(24)

print("opening relay")
relay.openRelay()

elapsedTimeSeconds = 0
fiveMinutesSeconds = 300
try:
	while True:
		if doorSensor.readSensor() == doorClosed:
			print("Door is closed!")
			elapsedTimeSeconds = 0
			relay.openRelay()
			time.sleep(10)
		else:
			if elapsedTimeSeconds < fiveMinutesSeconds:
				elapsedTimeSeconds += 100
				print(f'Door is open, timer = {elapsedTimeSeconds}')
			else:
				print("Door was open for 5 minutes, pressing switch!")
				relay.closeAndOpen()
				time.sleep(30)
			time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
	#sys.stdout.close()
	pass

#sys.stdout.close()
