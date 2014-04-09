'''
State base class
'''
import input as input
import libtcodpy as libtcod


class State:
  def __init__(self, disp):
    self.inputHandler = input.InputHandler()
    self.reset()
    
    self.disp = disp
    self.console = libtcod.console_new(disp.width, disp.height)
  
  def tick(self):
    print("Default tick handler")
    return self
  
  def registerStates(self, states) :
    self._states = states
  
  def reset(self):
    self.nextState = self
  
  def getConsole(self):
      return self.console