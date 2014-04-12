'''
World module

'''
import cell
import random
import libtcodpy as libtcod

class World:
  
  width = None
  height = None
  
  _cells = None
  
  c_lightOpen = libtcod.lightest_grey
  c_lightWall = libtcod.light_grey
  c_darkOpen = libtcod.darkest_grey
  c_darkWall = libtcod.darkest_grey * 0.5
  
  def __init__(self,w, h) :
    
    self.width = w
    self.height = h
    
    self._hm = libtcod.heightmap_new(w,h)
    self._cells = []
    
    self.initMap()
    self.resetMap()
    
    return
  
  
  def initMap(self) :
    print "Initing map"
    self.map = libtcod.map_new(self.width, self.height)
    for y in range(self.height) :
      for x in range(self.width) :
        c = cell.Cell(x,y)
        self._cells.append(c)
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
      print(x,y)
      c = self.getCell(x,y)
      if not c.passable:
        digCount = digCount - 1
        self._cells[x + y * self.width].dig(True)
    
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
              c.dig(False)
          else :
            if n <= caNeighboursStarve:
              c.dig(True)
    
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
    
  def getCell(self,x, y) :
    
    try:
      c = self._cells[x + y * self.width]
      return c
    except:
      return None
    
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
  
  def render(self, console) :
    # Draw each cell...
    for c in self._cells:
      # Our actual position on the screen, offset by 1 for the frame...
      y = 1 + c.y
      x = 1 + c.x
      libtcod.console_set_char_background(console, x, y, getattr(libtcod, c.color))
      
      
  
  def getCells(self) :
    return self._cells