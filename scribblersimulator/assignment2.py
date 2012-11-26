import time
from myro import *
rdyToTurn = 0
start_time = time.time()

def hasObstacle(p):
	a,b = p
	return a==0 or b==0

_getIR = getIR
def getIR():
	a,b = _getIR()
	return a,b
	
robspeed = 0.3
def stage1():
	print 'STAGE 1'
	while not hasObstacle(getIR()):
		backward(robspeed)
		# stage 3
		#print time.time() - start_time %2
		if (time.time() - start_time) %5 < .5:
			while not hasObstacle(getIR()):
				motors(robspeed,-robspeed)
			break
	time.sleep(1)
	stop()
	stage2()



def stage2():
	print 'STAGE2'
	while True:
		while hasObstacle(getIR()):
			motors(-robspeed,robspeed)
		#stop()
		time.sleep(1)
		stop()
		break
		# TODO: OVERTURN

	global rdyToTurn
	rdyToTurn = rdyToTurn + 1
	stage1()

def runAI():
	#starty = 
	while not hasObstacle(getIR()):
		backward(robspeed)
	stop()
	stage2()

init ('/dev/tty.IPRE6-197927-DevB')
runAI()
