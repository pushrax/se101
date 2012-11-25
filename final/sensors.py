from myro import *
from math import *
import time

class Sensors:
  def __init__(self, _robot):
    self.robot = _robot

  def getSensors(self):
    get1 = self.robot.get("obstacle")
    get2 = self.robot.get("obstacle")
    result = (get1[0] + get1[1] + get1[2]) > 1000 and (get2[0] + get2[1] + get2[2]) > 1000
    # TODO: Populate collision map
    return result