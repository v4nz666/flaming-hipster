'''
Cell module

'''
class Cell :
  
  def __init__(self,x, y) :
    self.x = x
    self.y = y
    self.reset()
  
  def reset(self):
    self.color = b'black'
    self.passable = False
    self.discovered = False
    self.items = []
  
  def dig(self, passable) :
    self.passable = passable
    if  self.passable:
      self.color = b'grey'
    else :
      self.color = b'black'
  
  def addItem(self, item):
    self.items.append(item)