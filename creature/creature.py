
import libtcodpy as libtcod
from ai import Ai

class Creature:
  
  species = None
  char    = " "
  color   = None
  health  = 0
  damage  = 0
  defense = 0
  aiUpdate = 'aiUpdate'
  world   = None
  x = y   = None
  state   = None
  
  '''
  Expects options:
    {
      'species' : 'bat',
      'char'    : '^',
      'color'   : libtcod.black,
      'health'  : 10,
      'damage'  : 5,
      'defense' : 1
    }
  '''
  def __init__(self, options):
    
    self.species = options['species']
    self.health = options['health']
    self.damage = options['damage']
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
    
  def update(self, player):
    self.aiUpdate(player)
  
  def moveTo(self,x, y):
    newCell = self.world.getCell(x, y)
    if newCell.passable:
      self.cell.removeCreature(self)
      newCell.addCreature(self)
      self.x = x
      self.y = y
      self.cell = newCell
      
