'''
World module

'''
import cell
from items import Items
import random
import math
import libtcodpy as libtcod

class World:
  
  width = None
  height = None
  
  _cells = None
  
  c_lightOpen = libtcod.lightest_grey
  c_lightWall = libtcod.light_grey
  c_darkOpen = libtcod.darkest_grey
  c_darkWall = libtcod.darkest_grey * 0.5
  c_torch = libtcod.lightest_flame
  
  def __init__(self,w, h) :
    
    self.width = w
    self.height = h
    
    self._hm = libtcod.heightmap_new(w,h)
    self._cells = []
    self._anchors = []
    
    self.initMap()
    
    return
  
  def initMap(self) :
    print "Initing map"
    self.map = libtcod.map_new(self.width, self.height)
    for y in range(self.height) :
      for x in range(self.width) :
        c = cell.Cell(x,y)
        self._cells.append(c)
    self.resetMap()
    return
  
  def resetMap(self):
    print "Resetting map"
    self.map = libtcod.map_new(self.width, self.height)
    for y in range(self.height) :
      for x in range(self.width) :
        self._cells[x + y * self.width].reset()
    ### Hightmap generation
    #self.randomizeHeightmap()
    
    #for y in range(self.height) :
    #  for x in range(self.width) :
    
        #alt = libtcod.heightmap_get_value(self._hm, x, y)
        #self._cells[x + y * self.width].dig(alt > 1)
    
    ### Celular automaton generation
    caDigDensity = 0.4
    caNeighboursSpawn = 6
    caNeighboursStarve = 3
    caIterations = 5
    
    digCount = self.width * self.height * caDigDensity
    
    while digCount > 0:
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)
      c = self.getCell(x,y)
      if not c.passable:
        digCount = digCount - 1
        self._cells[x + y * self.width].empty()
    
    for i in range(caIterations):
      neighbours = [[None for _y in range(self.height)] for _x in range(self.width)]
      for y in range(self.height) :
        for x in range(self.width) :
          neighbours[x][y] = self.countWallNeighbours(x,y)
      
      for y in range(self.height) :
        for x in range(self.width) :
          c = self.getCell(x, y)
          n = neighbours[x][y]
          if c.passable :
            if n >= caNeighboursSpawn:
              c.fill()
          else :
            if n <= caNeighboursStarve:
              c.empty()
    self._addWater()
    print "Done."
    return
  
  def countWallNeighbours(self,x, y) :
    n = 0
    for _x in range ( -1, 2 ):
      for _y in range ( -1, 2 ):
        if not _x and not _y:
          continue
        c = self.getCell(x + _x, y + _y)
        if c and not c.passable :
          n = n + 1
    return n
  
  def _addWater(self):
    
    waterProb = 0.0025
    waterCount = len(self._cells) * waterProb
    print "Water Count: " , waterCount, '/', len(self._cells)
    
    cellCount = len(self._cells) - 1
    
    while waterCount > 0 :
      i = random.randint(0, cellCount)
      c = self._cells[i]
      if c.passable and not c.hasItem(Items.Water):
        c.addItem(Items.Water)
        print "Water left: ", waterCount
        waterCount -= 1
    
  def getCell(self,x, y) :
    
    try:
      c = self._cells[x + y * self.width]
      return c
    except:
      return None
  
  def addAnchor(self, x, y):
    if not self.anchorAt(x,y):
      c = self.getCell(x,y)
      c.addItem(Items.Anchor)
  def anchorAt(self, x, y) :
    c = self.getCell(x,y)
    print "Anchor Check", c.items
    return Items.Anchor in c.items
  
  def passable(self, x, y):
    try:
      return self._cells[x + y * self.width].passable
    except IndexError:
      return False
  
  def randomizeHeightmap(self) :
    print "Setting up heightmap"
    hills = 1000
    hillSize = 7
    
    halfX = self.width / 2
    halfY = self.height / 2
    libtcod.heightmap_clear(self._hm)
    for i in range(hills) :
      size = random.randint(0,hillSize)
      
      hillX1 = random.randint(0,halfX - hillSize / 2)
      hillY1 = random.randint(0,self.height)
      
      hillX2 = random.randint(halfX + hillSize / 2, self.width)
      hillY2 = random.randint(0,self.height)
      
      libtcod.heightmap_add_hill(self._hm,hillX1, hillY1, size, size)
      libtcod.heightmap_add_hill(self._hm,hillX2, hillY2, size, size)
    
    libtcod.heightmap_normalize(self._hm, 0.0, 2.0)
  
  def calculateOffset(self, y, frame):
    
    if y < frame.innerHeight / 2:
      self.yOffset = 0
    elif y >= self.height - frame.innerHeight / 2:
      self. yOffset = self.height - frame.innerHeight
    else:
      self.yOffset = y - frame.innerHeight / 2
    
  def render(self, frame, player = False) :
    # Loop over every row inside the frame
    for y in range(frame.innerHeight):
      for x in range(frame.innerWidth + 1):
        c = self._cells[x + (y + self.yOffset) * self.width]
        
        # First draw the background color (black/grey)
        frame.setBgColor(x, y, c.color, libtcod.BKGND_SET)
        
        # Render the top item, if there are any here
        if len(c.items) > 0 and libtcod.map_is_in_fov(self.map, c.x, c.y):
          item = c.items[len(c.items)-1]
          frame.putChar(x, y, item.char, item.color)
        
        if player:
          self.renderPlayerOverlay(frame, player, c)
  
  def renderPlayerOverlay(self, frame, player, cell):
    
    visible = libtcod.map_is_in_fov(self.map, cell.x, cell.y)
      
    if visible:
      cell.discovered = True
      intensity = self.calculateIntensity(player, cell.x, cell.y)
      
      if cell.passable:
        color = self.c_lightOpen * self.c_torch
      else:
        color = self.c_lightWall * self.c_torch
    else:
      intensity = 1
      if not cell.discovered:
        color = libtcod.black
      else:
        if cell.passable:
          color = self.c_darkOpen
        else:
          color = self.c_darkWall
        
        rgb = 255 - ((cell.y * 255) / self.height)
        
        overlayColor = libtcod.Color(rgb, rgb, rgb)
        color = overlayColor * color
        
    frame.setBgColor(cell.x, cell.y - self.yOffset, color, libtcod.BKGND_ALPHA(intensity))
    
    y = player.y - self.yOffset
    x = player.x
    frame.putChar(x, y, '@', b'white')
    
  def calculateIntensity(self, player, x, y):
    intensity = 1
    
    deltaX = player.x - x
    deltaY = player.y - y
    
    distance = math.sqrt(math.pow(deltaX,2) + math.pow(deltaY, 2))
    
    if distance > 0:
      intensity = 1 - math.pow(distance / player.torchStrength, 2)
      intensity = 1.0 / 4.0 + (3*intensity) / 4
    return intensity
  
    
  def dig(self, x, y, player):
    if self.getCell(x, y).dig():
      libtcod.map_set_properties(self.map, x, y, True, True)
      return True
    else:
      return False
    
  
  def getCells(self) :
    return self._cells