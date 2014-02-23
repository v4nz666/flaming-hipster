'''
Cell module

'''
class Cell :
  
  def __init__(self,x, y) :
    self.x = x
    self.y = y
    
    self.even = not ( x + y ) % 2
    
    if self.even :
      self.color = b'red'
    else :
      self.color = b'blue'
    
    pass
