'''
Cell module

'''
class Cell :
  
  def __init__(self,x, y) :
    self.x = x
    self.y = y
    self.health = 1
    self.reset()
  
  def reset(self):
    self.color = b'black'
    self.passable = False
    self.discovered = False
    self.items = []
    self.creatures = []
  
  def dig(self) :
    if self.health > 0:
      self.health -= 1
      return False
    else:
      self.empty()
      return True
  
  def empty(self):
    self.passable = True
    self.color = b'grey'
  
  def fill(self):
    self.passable = False
    self.color = b'black'
  
  def addItem(self, item):
    self.items.append(item)
  
  def removeItem(self, item):
    self.items.remove(item)
  
  def addCreature(self, creature):
    print "Creature added!"
    self.creatures.append(creature)
  
  def removeCreature(self, creature):
    self.creatures.remove(creature)
  
  
  def hasItem(self, item):
    return item in self.items
  
  def hasItems(self):
    return len(self.items) > 0
  