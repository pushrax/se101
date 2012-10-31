from myro import *
import time
from math import *

init ('/dev/tty.IPRE6-197927-DevB')
robot = myro.globvars.robot
rospeed = 1
forward(rospeed)
d_left = (-rospeed,0)
d_right = (0,-rospeed)
rightTurn = 89

px,py = 0,0
angle = 0

def hasObstacle(p):
	a,b,c = robot.getObstacle()
	print a,b,c
	return b > 80

def stage1():
	global px,py,angle
	while not hasObstacle(robot.getIR()):
		print 'unobstacled'
		forward(rospeed,.5)
		px,py = px+.5*cos(angle),py+.5*sin(angle)
	print 'moving to stage2'
	stop()
	robot.setTurn(-rightTurn,'by','deg')
	angle += -pi/2
	#time.sleep(3)
	time.sleep(3)
	stage2()

def stage2():
	global px,py,angle
	while True:
		while not hasObstacle(robot.getIR()):
			forward(rospeed,3)
			px,py = px+3*cos(angle),py+3*sin(angle)
			if py == 0:
				robot.setTurn(int(-angle*180/pi),'by','deg')
				time.sleep(3)
				robot.forward(rospeed)
				return
			stop()
			robot.setTurn(rightTurn,'by','deg')
			angle += pi/2
			time.sleep(3)
			if hasObstacle(robot.getIR()):
				robot.setTurn(-rightTurn,'by','deg')
				angle += -pi/2
				time.sleep(3)

		#stop()
	stage1()

stage1()