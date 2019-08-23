from ESC import ESC
import os
os.system("sudo pigpiod")
import pigpio
import time

class MovementController:
	
	max = 2000
	min = 700

	def __init__(self):
		self.pi = pigpio.pi()
		self.brakeESC = new ESC(4, pi)
		self.rightESC = new ESC(6, pi)
		self.leftESC = new ESC(8, pi)

	def arm(self):
		self.brakeESC.setSpeed(0)
		self.rightESC.setSpeed(0)
		self.leftESC.setSpeed(0)
		time.sleep(1)
		self.brakeESC.setSpeed(max)
		self.rightESC.setSpeed(max)
		self.leftESC.setSpeed(max)
		time.sleep(1)
		self.brakeESC.setSpeed(min)
		self.rightESC.setSpeed(min)
		self.leftESC.setSpeed(min)
		time.sleep(1)

	# strSpeed = -1000 - 1000
	# right/left = 0 - 100 
	def move(self, strSpeed, right, left):
		
