'''
Cell module

'''
class Cell :
  
  def __init__(self,x, y) :
    self.x = x
    self.y = y
    
    self.alt = 0
    
    self.even = not ( x + y ) % 2
    
    if self.even :
      self.color = b'red'
    else :
      self.color = b'blue'
  
  def initColor(self) :
    if self.alt > 1 :
      self.color = b'dark_green'
    else :
      self.color = b'darker_blue'