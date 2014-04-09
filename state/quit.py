import sys

'''
quit State
'''
from state import State

class Quit(State):
  #TODO optional parameter for disp? not used here...
  def __init__(self, disp):
    State.__init__(self,disp)
  
  def tick(self):
    print "Quiting"
    sys.exit()