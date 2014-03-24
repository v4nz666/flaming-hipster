'''
State base class
'''
import input as input

class State:
  def __init__(self):
    self.inputHandler = input.InputHandler()
  
  def tick(self):
    print("Default tick handler")
    return False