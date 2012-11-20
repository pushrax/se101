from myro import *
import sys
sys.path.append(".")

from movement import *

init('COM3')

r = myro.globvars.robot
m = Movement(r)