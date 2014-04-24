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
  clippedRopes = []
  
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
      
      (newX, newY) = self.anchoredMove(newX, newY)
    
    self.x = newX
    self.y = newY
  
  def anchoredMove(self, newX, newY):
    
    # Moving to the last-visited tile, remove the current tile from the list, and 
    # regain a clippedRope
    last = len(self.clippedRopes) - 1
    if last > 0 and self.clippedRopes[last - 1] == (newX, newY):
        self.clippedRopes.pop()
    # Otherwise, if we have more ropes, do our anchor/jump checks
    elif len(self.clippedRopes) < self.ropes:
      # Already anchored wall, move onto it, and extend our rope path
      if self.world.anchorAt(newX, newY):
        self.clippedRopes.append((newX, newY))
      # Non-anchored wall, but we have anchors. Add an anchor, and extend our rope path
      elif self.anchors > 0:
        self.world.addAnchor(newX, newY)
        self.clippedRopes.append((newX, newY))
        self.anchors = self.anchors - 1
      # Non-anchored wall, and no anchors left, check if there is ground to jump to
      else:
        # No anchors left, but there's ground below the cell we're heading to.
        if not self.world.passable(newX, newY + 1):
          print "No looking back!"
          self.detach()
        # No anchor already mounted, and no solid ground to jump to - can't go that way
        else:
          newX = self.x
          newY = self.y
    
    # No ropes left, but there's ground to jump to.
    elif not self.world.passable(newX, newY + 1):
      print "No looking back!"
      self.detach()
        
    # No ropes left, and no solid ground to jump  to, cant go that way
    else:
      newX = self.x
      newY = self.y
    
    return (newX, newY)
  #end anchoredMove
  
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
    # Already an anchor here, just clip into it
    if self.world.anchorAt(self.x, self.y):
      self.affectedByGravity = False
      self.anchored = True
      self.clippedRopes.append((self.x, self.y))
    # We've got anchors, mount an anchor and clip in,
    elif self.anchors > 0:
      self.affectedByGravity = False
      self.anchored = True
      self.world.addAnchor(self.x, self.y)
      self.anchors = self.anchors - 1
      self.clippedRopes.append((self.x, self.y))
    
  def detach(self):
    self.affectedByGravity = True
    self.clippedRopes = []
    self.anchored = False