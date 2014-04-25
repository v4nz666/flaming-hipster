'''
Display

'''
import libtcodpy as libtcod
import math

class Player():
  
  def __init__(self, x, y, world) :
    self.x = x
    self.y = y
    self.world = world
    
    self.ropes   = 8
    self.anchors = 32
    self.anchored = False
    self.clippedRopes = []
    
    self.timer = 0
    
    self.health = 100.0
    self.healthStep = 1
    self.healthInterval = 120
    self.torchStrength = 6
  
  def update(self):
    self.timer = self.timer + 1
    if not self.timer % self.healthInterval:
      self.health = self.health - self.healthStep
    
  
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
      self.anchored = True
      self.clippedRopes.append((self.x, self.y))
    # We've got anchors, mount an anchor and clip in,
    elif self.anchors > 0:
      self.anchored = True
      self.world.addAnchor(self.x, self.y)
      self.anchors = self.anchors - 1
      self.clippedRopes.append((self.x, self.y))
    
  def detach(self):
    self.clippedRopes = []
    self.anchored = False