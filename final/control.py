from movement import *
from sensors import *

class Control:

	def __init__(self, _robot):
		self.robot = _robot
		self.robot.grid = [[0 for i in xrange(10)] for j in xrange(10)]
		self.movement = movement.Movement(_robot)
		s = Sensors(r)
		m = Movement(r, s)

	def run(self):
		self.movement.goto(10, 10)
