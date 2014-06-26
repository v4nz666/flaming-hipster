import item
import creature
import ai
import libtcodpy as libtcod

class Spawner(item.Item):
  
  def __init__(self, world, options):
    item.Item.__init__(self, options['species'] + ' Spawner', '.', 'black')
    self.world = world
    
    #creature constructor options
    self.options = options
    
    self.spawnRate = 25
    self.ticks = 1
    self.maxCreatures = 2
    self.creatureCount = 0
    
    self.affectedByGravity = False
    self.collectible = False
    
  def setCoords(self, x, y):
    self.x = x
    self.y = y
    print "coords set"
  
  def update(self):
    spawn = False
    
    if self.creatureCount >= self.maxCreatures:
      pass
    elif self.ticks % self.spawnRate != 0:
      self.ticks += 1
    else:
      self.creatureCount += 1
      self.ticks = 1
      print "spawn"
      spawn = True
      
    if spawn:
      c = creature.Creature(self.options)
      c.spawn(self.x, self.y)
      self.world.addCreature(c)
    
