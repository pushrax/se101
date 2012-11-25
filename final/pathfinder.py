
class Pathfinder:
	grid = []
	def __init__(self):
		self.grid = [[False for i in xrange(10)] for j in xrange(10)]

	def pathTo(self, x, y):
		path = [(1, 1), (x, y)]
		return path

	def addObstacle(self, x, y):
		self.grid[x][y] = True
