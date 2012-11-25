import sys
from myro import *
from control import *

sys.path.append(".")

if len(sys.argv) == 2:
	init(sys.argv[1])

	r = myro.globvars.robot
	c = Control(r)
	c.run()

else:
	print "Usage: run <init path>"
