from myro import *
import sys

from movement import *
from sensors import *

init('COM3')

r = myro.globvars.robot
s = Sensors(r)
m = Movement(r, s)