from myro import *
from math import *
from sensors import *
import time

class Movement:
	# Degrees per 360 degree turn
	calibrationT = 359
	# Encoder ticks per 30 cm
	calibrationF = 1200

	absangle = 0
	absx = calibrationF / 2
	absy = calibrationF / 2

	stop = False
	moving = False

	def __init__(self, _robot):
		self.robot = _robot
		self.sensors = Sensors(_robot, self)
		self.pathQueue = Queue()

	def isMoving(self):
		tmp = self.robot.getEncoders(True)
		return tmp[0] != 0 or tmp[1] != 0

	def turn(self, angle, relative=True):
		print "Turn:", angle
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
		print "Forward:", distance
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
				return False
			self.robot.translate(speed)
		self.robot.stop()
		return True

	def goto(self, x, y):
		print "Goto:", x, y
		relx = x - self.absx
		rely = y - self.absy
		dist = math.hypot(relx, rely)
		result = True
		if dist > 50:
			self.turn(math.degrees(math.atan2(relx, rely)), False)
			result = self.forward(dist)
		return result

	def gotoTile(self, tilex, tiley):
		self.moving = True
		path = self.robot.pathfinder.path((int(self.robot.pathfinder.width / 2 + self.absx / self.calibrationF), int(self.robot.pathfinder.height / 2 + self.absy / self.calibrationF)), (self.robot.pathfinder.width / 2 + tilex, self.robot.pathfinder.height / 2 + tiley))
		self.pathQueue.put(path)
		print path
		if path != None:
			for pp in path:
				print "Tile:", pp
				if not self.goto((pp[0] - self.robot.pathfinder.width / 2) * self.calibrationF + self.calibrationF / 2, (pp[1] - self.robot.pathfinder.height / 2) * self.calibrationF + self.calibrationF / 2):
					self.stopMove()
					self.gotoTile(tilex, tiley)
					self.moving = False
					return
		self.moving = False


	def stopMove(self):
		print "stop"
		self.robot.stop()
		self.stop = True
		self.moving = False