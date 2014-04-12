'''
Display

'''
from item import Item
import libtcodpy as libtcod
import math

class Player:

  def __init__(self, x, y, world) :
    self.x = x
    self.y = y
    self.world = world
    #self.seenMap = libtcod.map_new(world.width, world.height)
    
    self.calculate_fov = True
    self.torchStrength = 6
    self.torchColor = libtcod.lightest_flame#* libtcod.lightest_flame
  
  def update(self):
    try:
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
      intensity = 1
      
      if visible:
        c.discovered = True
        
        deltaX = self.x - c.x
        deltaY = self.y - c.y
        
        distance = math.sqrt(math.pow(deltaX,2) + math.pow(deltaY, 2))
        
        if distance > 0:
          intensity = 1 - math.pow(distance / self.torchStrength, 2)
          intensity = 1.0 / 4.0 + (3*intensity) / 4
        #print"dx, dy, d, d/tS, i:", (deltaX, deltaY, distance, distance / self.torchStrength, intensity)
        
        if c.passable:
          color = self.world.c_lightOpen * self.torchColor
        else:
          color = self.world.c_lightWall * self.torchColor
      else:
        if not c.discovered:
          color = libtcod.black
        else:
          if c.passable:
            color = self.world.c_darkOpen# + libtcod.darker_grey
          else:
            color = self.world.c_darkWall
      libtcod.console_set_char_background(console, c.x+1, c.y+1, color, libtcod.BKGND_ALPHA(intensity))
    
    y = 1 + self.y
    x = 1 + self.x
    libtcod.console_put_char(console, x, y, '@')
  
  def move(self, dx, dy):
    self.x = self.x + dx
    self.y = self.y + dy
    
    if self.x < 0 :
      self.x = 0
    elif self.x > self.world.width:
      self.x = self.world.width
    
    if self.y < 0 :
      self.y = 0
      print "Too High"
    elif self.y > self.world.height:
      self.y = self.world.height
      print "Too low"
  
  def mvUp(self):
    self.move(0, -1)
  def mvDn(self):
    print "Down from[", self.y, "]"
    self.move(0, 1)
    print "Down to  [", self.y, "]"
    
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
