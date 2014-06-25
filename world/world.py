'''
World module

'''
import random
import math
import libtcodpy as libtcod
import types
import creature
import ai

import cell
from items import Items

class World:
  
  width = None
  height = None
  
  _cells = None
  
  _creatures = []
  
  c_lightOpen = libtcod.lightest_grey
  c_lightWall = libtcod.light_grey
  c_darkOpen = libtcod.darkest_grey
  c_darkWall = libtcod.darkest_grey * 0.5
  c_torch = libtcod.desaturated_flame
  #torch alpha
  a_torch = 0.5
  
  def __init__(self,w, h) :
    
    self.width = w
    self.height = h
    
    self._hm = libtcod.heightmap_new(w,h)
    self._cells = []
    self._anchors = []
    self._spawners = []
    
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
    self._creatures = []
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
    self._addOres()
    self._addSpawners()
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
    self._addItems(Items.Water, True, 0.002)
    
  def _addOres(self):
    self._addItems(Items.Iron, False, 0.0015)
    self._addItems(Items.Coal, False, 0.0025)
  
  def _addItems(self, item, passable, prob = None, count = None, minDepth = None, maxDepth = None):
    if count:
      count = count
    elif prob:
      count = len(self._cells) * prob
    else:
      raise Exception("Must supply prob or count")
    
    cellCount = len(self._cells) - 1
    
    while count > 0 :
      i = random.randint(0, cellCount)
      c = self._cells[i]
      if c.passable == passable and not c.hasItem(item):
        if minDepth and not c.y >= minDepth:
          continue
        if maxDepth and not c.y <= maxDepth:
          continue
        
        if type(item) == types.FunctionType:
          item = item()
        
        c.addItem(item)
        if isinstance(item, creature.Spawner):
          item.setCoords(c.x, c.y)
        count -= 1
  
  def _addSpawners(self):
    
    def batSpawner():
      return creature.Spawner(self, {
        'species' : 'Bat',
        'char'    : '^',
        'color'   : 'black',
        'health'  : 10,
        'damage'  : 5,
        'defense' : 1,
        'world'   : self,
        'aiUpdate' : ai.Ai.batAiUpdate
      })
    for i in range(10):
      spawner = batSpawner()
      self._spawners.append(spawner)
      self._addItems(
        spawner,
        True,
        None, # prob
        1,    # count
        1,    # minDepth
        50    # maxDepth
      )

    #def spiderSpawner():
      #return creature.Spawner(self, {
        #'species' : 'Cave Spider',
        #'char'    : 'x',
        #'color'   : 'black',
        #'health'  : 15,
        #'damage'  : 7,
        #'defense' : 3
      #})
    #for i in range(5):
      #spawner = spiderSpawner()
      #self._spawners.append(spawner)
      #self._addItems(
        #spawner,
        #True,
        #None, # prob
        #1,    # count
        #20,   # minDepth
        #int((3 * self.height) / 4)    # maxDepth
      #)
  
  def addCreature(self, c):
    if not isinstance(c, creature.Creature):
      raise Exception("Invalid creature")
    self._creatures.append(c)
    print "Creature added. Length: " + str(len(self._creatures))
  
  def removeCreature(self, c):
    self._creatures.remove(c)
  
  def getCell(self,x, y) :
    try:
      c = self._cells[x + y * self.width]
      return c
    except:
      return None
  
  def addAnchor(self, x, y):
    c = self.getCell(x,y)
    if not c.hasItem(Items.Anchor):
      c.addItem(Items.Anchor)
  
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
  
  def update(self):
    for c in self._cells:
      if len(c.items) > 0 :
        for item in c.items:
          if c.passable and item.affectedByGravity:
            cellBelow = self.getCell(c.x, c.y+1)
            if cellBelow and cellBelow.passable:
              cellBelow.addItem(item)
              c.removeItem(item)
    for s in self._spawners:
      s.update()
    for cr in self._creatures:
      cr.update()
  
  def render(self, frame, player = False) :
    # Loop over every row inside the frame
    for y in range(frame.innerHeight):
      yIndex = (y + self.yOffset) * self.width
      for x in range(frame.innerWidth + 1):
        c = self._cells[x + yIndex]
        
        # First draw the background color (black/grey)
        frame.setBgColor(x, y, c.color, libtcod.BKGND_SET)
        
        # If we're in game mode, show the items, and render the player's torch overlay.
        if player:
          if libtcod.map_is_in_fov(self.map, c.x, c.y):
            # Render the top item, if there are any here
            if len(c.items) > 0:
              item = c.items[len(c.items)-1]
              frame.putChar(x, y, item.char, item.color)
            if len(c.creatures) > 0:
              creature = c.creatures[len(c.creatures)-1]
              frame.putChar(x, y, creature.char, creature.color)
            
            
          self.renderPlayerOverlay(frame, player, c)
          
  def renderPlayerOverlay(self, frame, player, cell):
    
    visible = libtcod.map_is_in_fov(self.map, cell.x, cell.y)
      
    if visible:
      cell.discovered = True
      intensity = self.calculateIntensity(player, cell.x, cell.y)
      
      if cell.passable:
        color = libtcod.color_lerp(self.c_lightOpen, self.c_torch, self.a_torch)
      else:
        color = libtcod.color_lerp(self.c_lightWall, self.c_torch, self.a_torch)
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