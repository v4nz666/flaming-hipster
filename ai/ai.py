import libtcodpy as libtcod

class Ai():
  world = None
  player = None
  
  first = True
  def __init__(self, creature, world):
    self.creature = creature
    self.world = world
    
    self.path = libtcod.path_new_using_map(self.world.map)
    
    
  def aiUpdate(self):
    if self.first:
      print "Default ai Update"
      self.first = False
    pass
  
  def batAiUpdate(self, player):
    if self.first:
      print "Bat ai Update"
      self.first = False
    
    libtcod.path_compute(self.path, self.creature.x, self.creature.y, player.x, player.y)
    (x, y) = libtcod.path_walk(self.path, False)
    if x and y:
      self.creature.moveTo(x, y)
    else:
      print "no path"
