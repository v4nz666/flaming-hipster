'''
State base class
'''
import input as input
import libtcodpy as libtcod


class State:
  def __init__(self, disp):
    self.inputHandler = input.InputHandler()
    
    self.disp = disp
    self.console = libtcod.console_new(disp.width, disp.height)
    
    self.reset()
  
  def tick(self):
    print("Default tick handler")
    return self
  
  def registerStates(self, states) :
    self._states = states
  
  def reset(self):
    self.nextState = self
    libtcod.console_clear(self.console)
  
  def getConsole(self):
      return self.console
  
  def beforeTransition(self):
    pass
  