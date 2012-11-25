from movement import *
from sensors import *

class Control:

	def __init__(self, _robot):
		_robot.pathfinder = pathfinder.Pathfinder()
		self.movement = movement.Movement(_robot)
		s = Sensors(_robot)
		m = Movement(_robot, s)
		self.robot = _robot

	def run(self):
		self.movement.goto(10, 10)
