from movement import *
from pathfinder import *

class Control:

	def __init__(self, _robot):
		_robot.pathfinder = Pathfinder()
		self.movement = movement.Movement(_robot)
		self.robot = _robot

	def run(self):
		self.movement.goto(10, 10)
