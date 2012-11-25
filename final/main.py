from myro import *
from control import *
import socket
import threading

class SocketThread(threading.Thread):
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(("", 5005))
		s.listen(1)

		while 1:
			conn, addr = s.accept()
			while 1:
			    data = conn.recv(100)
			    if not data: break
			    tmp = data[:-1].split(" ")
			    print tmp
			    if tmp[0] == "moveto" and not c.movement.moving:
			    	c.targetx = int(tmp[1])
			    	c.targety = int(tmp[2])
			    conn.send("pos " + str(int(c.movement.absx)) + " " + str(int(c.movement.absy)) + " " + str(int(c.movement.absangle)) + "\n")
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