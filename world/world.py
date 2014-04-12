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
    for y in range(self.height) :
      for x in range(self.width) :
        c = cell.Cell(x,y)
        self._cells.append(c)
    return
  
  def resetMap(self):
    print "Resetting map"
    self.randomizeHeightmap()
    for y in range(self.height) :
      for x in range(self.width) :
        alt = libtcod.heightmap_get_value(self._hm, x, y)
        self._cells[x + y * self.width].dig(alt > 1)
    
    
    
    return
  
  #def getCell(self, x, y) :
    #return self._cells[x + y * self.width]
  
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
    
  def getCells(self) :
    return self._cells