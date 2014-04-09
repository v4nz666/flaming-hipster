'''
menu State
'''
from state import State
import libtcodpy as libtcod

class Menu(State):
  def __init__(self, disp):
    State.__init__(self, disp)
    
  def tick(self):
    return self