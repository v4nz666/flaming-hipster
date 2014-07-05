import libtcodpy as libtcod

class Ai():
  world = None
  player = None
  
  def __init__(self, creature, world):
    self.creature = creature
    self.world = world
    
    self.path = libtcod.path_new_using_map(self.world.map)
    
    
  def aiUpdate(self):
    pass
  
  def batAiUpdate(self, player):
    path = libtcod.path_compute(self.path, self.creature.x, self.creature.y, player.x, player.y)
    if path:
      length = libtcod.path_size(self.path)
      if length > 1:#self.creature.attackRange
        (x, y) = libtcod.path_walk(self.path, False)
        self.creature.moveTo(x, y)
      else:
        self.creature.attackCreature(player)
        
    else:
      pass
