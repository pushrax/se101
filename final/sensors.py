from myro import *
from math import *
import time

class Sensors:
	def __init__(self, _robot, _movement):
		self.robot = _robot
		self.movement = _movement

	def getSensors(self):
		get1 = self.robot.get("obstacle")
		get2 = self.robot.get("obstacle")
		result = (get1[0] + get1[1] + get1[2]) > 1000 and (get2[0] + get2[1] + get2[2]) > 1000
		if result:
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
			print "Robot at:", int(self.robot.pathfinder.width / 2 + self.movement.absx / self.movement.calibrationF), int(self.robot.pathfinder.height / 2 + self.movement.absy / self.movement.calibrationF)
			print "Obstacle:", int(self.robot.pathfinder.width / 2 + self.movement.absx / self.movement.calibrationF + offx), int(self.robot.pathfinder.height / 2 + self.movement.absy / self.movement.calibrationF + offy)
			self.robot.pathfinder.addObstacle(
				int(self.robot.pathfinder.width / 2 + self.movement.absx / self.movement.calibrationF + offx),
				int(self.robot.pathfinder.height / 2 + self.movement.absy / self.movement.calibrationF + offy))
		return result