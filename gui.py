'''
GUI module

'''
import frame as frame

class Gui :
  
  def __init__(self, console) :
    self.console = console
    self.frames = {}
    
    return
  
  def addFrame(self, x ,y, w, h, name) :
    self.frames[name] = frame.Frame(self.console, x, y, w, h, name)
    
  
  def render(self):
    for key in self.frames:
      self.frames[key].renderFrame()
    
    for key in self.frames:
      self.frames[key].renderTitle()

    for key in self.frames:
      self.frames[key].printMessages()
  
  def getFrames(self) :
    return self.frames