from myro import *
from math import *
from sensors import *
import time

class Movement:
	# Encoder ticks per 90 degree turn
	ticksPer90 = 5.23
	# Encoder ticks per tile
	ticksPerTile = 1200

	absangle = 0
	absx = ticksPerTile / 2
	absy = ticksPerTile / 2

	stop = False
	moving = False

	def __init__(self, _robot):
		self.robot = _robot
		self.sensors = Sensors(_robot, self)
		self.pathQueue = Queue()

	def isMoving(self):
		tmp = self.robot.getEncoders(True)
		return tmp[0] != 0 or tmp[1] != 0

	def turn(self, angle):
		print "Turn:", angle
		angle -= self.absangle
		while angle > 180:
			angle -= 360
		while angle < -180:
			angle += 360
		aangle = abs(angle)
		self.stop = False
		self.robot.getEncoders(True)
		speed = -1
		while not self.stop and aangle > 2:
			tmp = self.robot.getEncoders(True)
			delta = (tmp[0] - tmp[1]) / 2.0
			delta /= float(self.ticksPer90)
			aangle -= math.fabs(delta)
			self.absangle -= delta

			if speed < 0:
				speed = 0.2
			elif aangle < 20:
				speed = 0.2
			elif aangle < 45:
				speed = 0.35
			else:
				speed = 0.5
			time.sleep(0.1)
			if angle > 0:
				self.robot.rotate(-speed)
			else:
				self.robot.rotate(speed)
		self.robot.stop()

	def forward(self, distance):
		print "Forward:", distance
		self.stop = False
		self.robot.getEncoders(True)
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
				self.robot.stop()
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
			self.turn(math.degrees(math.atan2(relx, rely)))
			result = self.forward(dist)
		return result

	def gotoTile(self, tilex, tiley):
		self.moving = True
		path = self.robot.pathfinder.path((int(self.robot.pathfinder.width / 2 + self.absx / self.ticksPerTile), int(self.robot.pathfinder.height / 2 + self.absy / self.ticksPerTile)), (self.robot.pathfinder.width / 2 + tilex, self.robot.pathfinder.height / 2 + tiley))
		if path != None:
			self.pathQueue.put(path)
			print path
			for pp in path:
				print "Tile:", pp
				if not self.goto((pp[0] - self.robot.pathfinder.width / 2) * self.ticksPerTile + self.ticksPerTile / 2, (pp[1] - self.robot.pathfinder.height / 2) * self.ticksPerTile + self.ticksPerTile / 2):
					return self.gotoTile(tilex, tiley)
				else:
					self.moving = False
					return True
		else:
			self.moving = False
			return False