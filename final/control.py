from movement import *
from pathfinder import *
from music import *
import time

class Control:

	targetx = 0
	targety = 0

	def __init__(self, robot):
		robot.pathfinder = Pathfinder()
		robot.music = Music(robot)
		self.movement = Movement(robot)
		self.robot = robot

	def run(self):
		while 1:
			if not self.movement.moving:
				self.movement.gotoTile(self.targetx, self.targety)
			time.sleep(1)
