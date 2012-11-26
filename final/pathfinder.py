from heapq import *

class Pathfinder:
	grid = []
	def __init__(self):
		self.width = 100 # max x
		self.height = 100 # max y
		self.grid = [[(False, None) for i in xrange(self.height)] for j in xrange(self.width)]

	def path(self, start, end):
		if start == end:
			return None
		openHeap = [] # (heuristic + dist, dist, coord)
		heappush(openHeap, (0, 0, start))
		openSet = set([start])
		closedSet = set()

		def heuristic(a, b):
			return abs(a[0] - b[0]) + abs(a[1] - b[1]) # manhattan distance

		while openSet:
			h, dist, c = heappop(openHeap)
			if c == end:
				path = [c]
				while True:
					c = self.grid[c[0]][c[1]][1] # get parent
					if c == start:
						path.reverse()
						return path
					if c == None:
						return None
					path.append(c)

			openSet.remove(c)
			closedSet.add(c)
			for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
				nc = (c[0] + dx, c[1] + dy)
				if nc[0] < 0 or nc[1] < 0 or nc[0] >= self.width or nc[1] >= self.height:
					continue
				next = self.grid[nc[0]][nc[1]]
				if not next[0] and nc not in closedSet and nc not in openSet:
					new = dist + 1, dist + 1, nc
					heappush(openHeap, new)
					openSet.add(nc)
					self.grid[nc[0]][nc[1]] = (next[0], c) # set parent
		return None

	def addObstacle(self, x, y):
		self.grid[x][y] = (True, None)

# a simple test
# p = Pathfinder()
# a = [
# 	[0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
# 	[0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
# 	[0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
# 	[1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
# 	[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]
# b = [[0 for i in xrange(10)] for j in xrange(10)]
# for i in xrange(10):
# 	for j in xrange(10):
# 		if a[i][j] == 1:
# 			p.addObstacle(i, j)
# 			b[i][j] = 1
# pp = p.path((0, 0), (9, 9))

# if pp != None:
# 	for d in pp:
# 		b[d[0]][d[1]] = 2

# b[0][0] = 3
# b[9][9] = 3

# for d in b:
# 	l = ''
# 	for e in d:
# 		if e == 0:
# 			l += '  '
# 		if e == 1:
# 			l += '# '
# 		if e == 2:
# 			l += '. '
# 		if e == 3:
# 			l += 'x '
# 	print l