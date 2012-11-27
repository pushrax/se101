from myro import *
from control import *
import socket
import threading

def reset():
	c.movement.absangle = 0
	c.movement.absx = c.movement.ticksPerTile / 2
	c.movement.absy = c.movement.ticksPerTile / 2
	r.pathfinder.grid = [[(False, None) for i in xrange(r.pathfinder.height)] for j in xrange(r.pathfinder.width)]

class SocketThread(threading.Thread):
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(("", 5005))
		s.listen(1)

		while 1:
			conn, addr = s.accept()
			reset()
			print "Connected"
			while 1:
				data = conn.recv(100)
				if not data: break
				tmp = data[:-1].split(" ")
				if tmp[0] == "moveto":
					c.targetx = int(tmp[1])
					c.targety = int(tmp[2])
				conn.send("pos " + str(int(c.movement.absx)) + " " + str(int(c.movement.absy)) + " " + str(int(c.movement.absangle)) + "\n")
				try:
					obs = r.pathfinder.obstacleQueue.get_nowait()
					conn.send("block " + str(obs[0]) + " " + str(obs[1]) + "\n")
				except Empty:
					pass
				try:
					path = c.movement.pathQueue.get_nowait()
					buf = "path"
					for i in path:
						buf += " " + str(i[0]) + " " + str(i[1])
					print "sending:", buf
					conn.send(buf + "\n")
				except Empty:
					pass
			conn.close()

if len(sys.argv) == 2:
	init(sys.argv[1])

	r = myro.globvars.robot
	c = Control(r)

	t = SocketThread()
	t.start()

	c.run()

else:
	print "Usage: run <init path>"