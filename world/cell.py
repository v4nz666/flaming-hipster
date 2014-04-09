'''
Cell module

'''
class Cell :
  
  def __init__(self,x, y) :
    self.x = x
    self.y = y
    
    self.alt = 0
    self.passable = False
    self.even = not ( x + y ) % 2
  
  def initColor(self) :
    if self.alt > 1 :
      self.passable = True
      self.color = b'grey'
    else :
      self.color = b'black'