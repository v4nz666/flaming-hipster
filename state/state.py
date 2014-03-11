'''
State base class
'''

class State:
  def __init__(self, name):
    self.name = name
  
  def initInputs(self, inputs):
    self.inputs = inputs
    print "Inputs ", self.inputs
  
  def tick(self):
    print("Default tick handler, exiting")
    return False

# For Blocking input, override with a similar method
  #def tick(self):
    #key = libtcod.console_wait_for_keypress(True)
    #return self.handleInput(key)
  
  def handleInput(self,key):
    for name in self.inputs:
      print("Checking ", name)
      cmd = self.inputs[name]
      if ( cmd['key'] and cmd['key'] == key.vk ) or (
        cmd['ch'] and ( ord(cmd['ch'].lower()) == key.c or ord(cmd['ch'].upper()) == key.c ) ):
          return cmd['fn']()
    return self
