import sys

'''
quit State
'''
from state import State

class Quit(State):
  def __init__(self):
    State.__init__(self)
  
  def tick(self):
    print "Quiting"
    sys.exit()