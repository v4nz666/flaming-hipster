class InputHandler():
  def __init__(self):
    pass
  
  def initKeyInputs(self,inputs):
    self.inputs = inputs
    print "Inputs ", self.inputs
  
  def handleInput(self, cmd):
    print("Default input handler.")
    return