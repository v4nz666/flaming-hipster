'''
Cell module

'''
class Cell :
  
  def __init__(self,x, y) :
    self.x = x
    self.y = y
    
    self.passable = False
    self.even = not ( x + y ) % 2
  
  def dig(self, passable) :
    self.passable = passable
    if  self.passable:
      self.color = b'grey'
    else :
      self.color = b'black'