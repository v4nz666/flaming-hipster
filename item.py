class Item():
  def __init__(self, x, y, world):
    self.x = x
    self.y = y
    
    self.ch = " "
    
    self.world = world
    self.affectedByGravity = True
    