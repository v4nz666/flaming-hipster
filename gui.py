'''
GUI module

'''

class Gui :
  selectedX = 0;
  selectedY = 0;
  
  def __init__(self, board) :
    self.board = board
    return
  
  def selectionUp(self) :
    y = self.selectedY - 1;
    if y >= 0 :
      self.selectedY = y
  
  def selectionDn(self) :
    y = self.selectedY + 1;
    if y < self.board.height :
      self.selectedY = y
  
  def selectionLft(self) :
    x = self.selectedX - 1;
    if x >= 0 :
      self.selectedX = x
  
  def selectionRgt(self) :
    x = self.selectedX + 1;
    if x < self.board.width :
      self.selectedX = x


  def getSelected(self) :
    return (self.selectedX, self.selectedY)