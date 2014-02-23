'''
Board module

'''
import cell

class Board :
  
  width = None
  height = None
  
  _cells = None
  
  def __init__(self,w, h) :
    
    self.width = w
    self.height = h
    
    #Initialize an inner list for each x-position
    self._cells = []
    
    for y in range(h) :
      for x in range(w) :
        c = cell.Cell(x,y)
        self._cells.append(c)
    return
  
  def getCells(self) :
    return self._cells