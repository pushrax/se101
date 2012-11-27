from myro import *
from math import *
import time

class Sensors:
	def __init__(self, _robot, _movement):
		self.robot = _robot
		self.movement = _movement

	def getSensors(self):
		get = self.robot.get("obstacle")
		result = (get[0] + get[1] + get[2]) > 1000
		count = 0
		while result and count < 3:
			get = self.robot.get("obstacle")
			result = (get[0] + get[1] + get[2]) > 1000
			count += 1
		if count >= 3:
			offx = 0
			offy = 0
			if self.movement.absangle >= -45 and self.movement.absangle < 45:
				offy = 1
			elif self.movement.absangle >= 45 and self.movement.absangle < 135:
				offx = 1
			elif self.movement.absangle >= 135 and self.movement.absangle < 225:
				offy = -1
			else:
				offx = -1
			print "Obstacle:", int(self.robot.pathfinder.width / 2 + self.movement.absx / self.movement.ticksPerTile + offx), int(self.robot.pathfinder.height / 2 + self.movement.absy / self.movement.ticksPerTile + offy)
			self.robot.pathfinder.addObstacle(
				int(self.robot.pathfinder.width / 2 + self.movement.absx / self.movement.ticksPerTile + offx),
				int(self.robot.pathfinder.height / 2 + self.movement.absy / self.movement.ticksPerTile + offy))
			return True
		return False