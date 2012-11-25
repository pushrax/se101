from myro import *
from math import *
from sensors import *
import time

class Movement:
	# Degrees per 360 degree turn
	calibrationT = 359
	# Encoder ticks per 10 cm
	calibrationF = 1

	absangle = 0
	absx = 0
	absy = 0

	stop = False
	moving = False

	def __init__(self, _robot):
		self.robot = _robot
		self.sensors = Sensors(_robot)

	def isMoving(self):
		tmp = self.robot.getEncoders(True)
		return tmp[0] != 0 or tmp[1] != 0

	def turn(self, angle, relative=True):
		if not relative:
			angle -= self.absangle
		while angle > 180:
			angle -= 360
		while angle < -180:
			angle += 360
		tmp = (int) (-angle * self.calibrationT / 360)
		self.isMoving()
		self.robot.setTurn(tmp, 'by', 'deg')
		if tmp != 0:
			while not self.isMoving():
				time.sleep(0.05)
			while self.isMoving():
				time.sleep(0.5)
		self.absangle += angle
		while self.absangle > 180:
			self.absangle -= 360
		while self.absangle < -180:
			self.absangle += 360
		self.robot.setAngle((int) (self.absangle))

	def forward(self, distance):
		self.stop = False
		self.robot.getEncoders(True)
		start = self.robot.getPosition()
		speed = -1
		while not self.stop and distance > 50:
			tmp = self.robot.getEncoders(True)
			tmp = math.fabs((tmp[0] + tmp[1]) / 2)
			distance -= tmp
			tmp2 = math.radians(self.absangle)
			self.absx += math.sin(tmp2) * tmp
			self.absy += math.cos(tmp2) * tmp
			if speed < 0:
				speed = 0.1
			elif distance < 100:
				speed = 0.1
			elif distance < 200:
				speed = 0.5
			else:
				speed = 1
			if self.sensors.getSensors():
				break
			self.robot.translate(speed)
		self.robot.stop()

	def goto(self, x, y):
		self.moving = True
		relx = x - self.absx
		rely = y - self.absy
		dist = math.hypot(relx, rely)
		if dist > 50:
			self.turn(math.degrees(math.atan2(relx, rely)), False)
			self.forward(dist)
		self.moving = False


	def stop():
		self.stop = True
		self.moving = False