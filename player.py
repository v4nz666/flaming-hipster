'''
Display

'''
from item import Item
from rope import Rope
import libtcodpy as libtcod
import math

class Player(Item):

  ropes   = 8
  anchors = 32
  anchored = False
  clippedRopes = 0
  
  def __init__(self, x, y, world) :
    Item.__init__(self, x, y, world)
    
    self.torchStrength = 6
    self.torchColor = libtcod.lightest_flame
  
  def update(self):
    pass
  
  def render(self, console):
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
          
          rgb = 255 - ((c.y * 255) / self.world.height)
          
          overlayColor = libtcod.Color(rgb, rgb, rgb)
          color = overlayColor * color
          
      libtcod.console_set_char_background(console, c.x+1, c.y+1, color, libtcod.BKGND_ALPHA(intensity))
    
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
    
    if self.anchored:
      if self.clippedRopes < self.ropes:
        
        self.clippedRopes = self.clippedRopes + 1
        
        #already anchored wall, just move onto it
        if self.world.anchorAt(newX, newY):
          pass
        #non-anchored wall, but we have anchors
        elif self.anchors > 0:
          self.world.addAnchor(newX, newY)
          self.anchors = self.anchors - 1
        #no ropes left, but there's ground below the cell we're heading to. A one way trip until you restock on anchors
        elif not self.world.passable(newX, newY + 1):
          print "No looking back!"
          self.detach()
      # no ropes left, cant go that way
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
    if self.ropes > 0 :
      
      self.clippedRopes = 1
      
      # Already an anchor here, just clip into it
      if self.world.anchorAt(self.x, self.y):
        self.affectedByGravity = False
        self.anchored = True
        # We've got anchors, so clip in, and 
      elif self.anchors > 0:
        self.affectedByGravity = False
        self.anchored = True
        self.world.addAnchor(self.x, self.y)
        self.anchors = self.anchors - 1
        
  def detach(self):
    self.affectedByGravity = True
    self.clippedRopes = 0
    self.anchored = False