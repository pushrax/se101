from movement import *
from pathfinder import *
import time

class Control:

	targetx = 0
	targety = 0

	def __init__(self, _robot):
		_robot.pathfinder = Pathfinder()
		self.movement = Movement(_robot)
		self.robot = _robot

	def run(self):
		while 1:
			if not self.movement.moving:
				self.movement.gotoTile(self.targetx, self.targety)
			time.sleep(1)
