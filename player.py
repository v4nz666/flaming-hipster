'''
Display

'''
from item import Item
from rope import Rope
import libtcodpy as libtcod
import math

class Player(Item):

  ropes = 64
  hooks = 64
  anchoredRopes = []
  ropedOff = False
  
  def __init__(self, x, y, world) :
    Item.__init__(self, x, y, world)
    
    self.calculate_fov = True
    self.torchStrength = 6
    self.torchColor = libtcod.lightest_flame
  
  def update(self):
    try:
      if self.affectedByGravity:
        cellBelow = self.world.getCell(self.x, self.y + 1)
        if cellBelow.passable:
          self.mvDn()
    except:
      pass
  
  def render(self, console):
    if self.calculate_fov:
      libtcod.map_compute_fov(self.world.map, self.x, self.y, self.torchStrength, True, libtcod.FOV_SHADOW)
    for c in self.world.getCells():
      visible = libtcod.map_is_in_fov(self.world.map, c.x, c.y)
      
      if visible:
        c.discovered = True
        intensity = self.calculate_intensity(c.x, c.y)
        #print"dx, dy, d, d/tS, i:", (deltaX, deltaY, distance, distance / self.torchStrength, intensity)
        
        if c.passable:
          color = self.world.c_lightOpen * self.torchColor
        else:
          color = self.world.c_lightWall * self.torchColor
      else:
        intensity = 1
        if not c.discovered:
          color = libtcod.black
        else:
          if c.passable:
            color = self.world.c_darkOpen
          else:
            color = self.world.c_darkWall
      libtcod.console_set_char_background(console, c.x+1, c.y+1, color, libtcod.BKGND_ALPHA(intensity))
    
    
    for anchor in self.anchoredRopes:
      x = 1 + anchor[0]
      y = 1 + anchor[1]
      if libtcod.map_is_in_fov(self.world.map, x, y):
        intensity = 0.25 + ((3 * self.calculate_intensity(x, y)) / 4)

        libtcod.console_put_char(console, x, y, '"')
        libtcod.console_set_char_foreground(console, x, y, libtcod.white * intensity)
  
    y = 1 + self.y
    x = 1 + self.x
    libtcod.console_put_char(console, x, y, '@')
    
  def calculate_intensity(self,x, y):
    intensity = 1
    
    deltaX = self.x - x
    deltaY = self.y - y
    
    distance = math.sqrt(math.pow(deltaX,2) + math.pow(deltaY, 2))
    
    if distance > 0:
      intensity = 1 - math.pow(distance / self.torchStrength, 2)
      intensity = 1.0 / 4.0 + (3*intensity) / 4
    return intensity
  
  def move(self, dx, dy):
    newX = self.x + dx
    newY = self.y + dy
    
    if self.ropedOff:
      
      #already anchored wall
      if (newX, newY) in self.anchoredRopes:
        pass
      #non-anchored wall, but we have ropes
      elif self.ropes > 0:
        self.anchoredRopes.append((newX, newY))
        self.ropes = self.ropes - 1
      #non-anchored, and no ropes, cant go that way
      else:
        newX = self.x
        newY = self.y
      
    self.x = newX
    self.y = newY
    
  def mvUp(self):
    self.move(0, -1)
  def mvDn(self):
    self.move(0, 1)
    
  def mvRt(self):
    self.move(1, 0)
  def mvLt(self):
    self.move(-1, 0)
  
  def mvUpLft(self):
    self.move(-1, -1)
  def mvUpRgt(self):
    self.move(1, -1)
  
  def mvDnLft(self):
    self.move(-1, 1)
  def mvDnRgt(self):
    self.move(1, 1)
  
  def anchorRope(self):
    self.affectedByGravity = False
    self.ropedOff = True
    if self.ropes > 0 and (self.x, self.y) not in self.anchoredRopes:
      #attach the rope at our feet (y+1)
      self.anchoredRopes.append((self.x, self.y))
  
  def detach(self):
    self.affectedByGravity = True
    self.ropedOff = False