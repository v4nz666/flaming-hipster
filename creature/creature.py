
import libtcodpy as libtcod
from ai import Ai

class Creature:
  '''
  Expects options:
    {
      'species' : 'bat',
      'health'  : 10,
      'attack'  : 5,
      'defense' : 1
      'char'    : '^',
      'color'   : libtcod.black,
      'world'   : World instance
      'aiUpdate': Ai class method reference
    }
  '''
  def __init__(self, options):
    
    self.species = options['species']
    self.health = options['health']
    self.max_health = options['health']
    self.min_health = 0
    self.attack = options['attack']
    self.defense =  options['defense']
    self.char = options['char']
    self.color = options['color']
    
    self.world = options['world']
    self.ai = Ai(self, self.world)
    self.aiUpdate = getattr(self.ai, options['aiUpdate'])
    
  def spawn(self, x, y):
    self.x = x
    self.y = y
    self.cell = self.world.getCell(x,y)
    self.cell.addCreature(self)
  def die(self):
    self.cell.removeCreature(self)
    self.world.removeCreature(self)
  
  def update(self, player):
    self.aiUpdate(player)
  
  def attrDelta(self, attr, delta):
    if hasattr(self, attr):
  
      max = getattr(self, "max_" + attr)
      min = getattr(self, "min_" + attr)
      
      oldVal = getattr(self, attr)
      newVal = oldVal + delta
      if newVal > max:
        newVal = max
      elif newVal < min:
        newVal = min
      
      setattr(self, attr, newVal)
  ### attrDelta
  #############
  def attackCreature(self, target):
    rand = libtcod.random_new()
    damage = libtcod.random_get_int(rand, 0, self.attack)
    defense = libtcod.random_get_int(rand, 0, target.defense)
    
    delta = damage - defense
    if delta > 0:
      target.attrDelta('health', - delta)
      print self.species + " hit " + target.species + " for " + str(delta) + " damage! " +\
        str(target.health) + " health left"
      if target.health <= 0:
        target.die()
    
  
  def moveTo(self,x, y):
    newCell = self.world.getCell(x, y)
    if newCell.passable:
      self.cell.removeCreature(self)
      newCell.addCreature(self)
      self.x = x
      self.y = y
      self.cell = newCell
  