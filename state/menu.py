'''
menu State
'''
from state import State
import libtcodpy as libtcod

class Menu(State):
  def __init__(self, disp):
    self.disp = disp
    self.console = libtcod.console_new(disp.width, disp.height)
  
  def tick(self):
    
    return self