import time
import pigpio

class ESC:
	
	max = 2000
	min = 700

	def __init__(self, pin, pig):
		self.pin = pin
		self.pi = pig

	def setSpeed(self, speed):
		self.pi.set_servo_pulsewidth(self.pin, speed)
