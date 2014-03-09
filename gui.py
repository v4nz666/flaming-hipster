'''
GUI module

'''
import frame as frame

class Gui :
  selectedX = 0;
  selectedY = 0;
  
  def __init__(self, board, uiWidth) :
    
    #Main game board
    self.board = board
    
    #Our list of frames
    self.frames = [
      frame.Frame(0,0,board.width,board.height, 'Game Board'),
      frame.Frame(board.width + 1,0, uiWidth, board.height / 3 - 1, 'Friends'),
      frame.Frame(board.width + 1,board.height / 3, uiWidth, board.height / 3 - 1, 'Foes'),
      frame.Frame(board.width + 1,2 * board.height / 3, uiWidth, board.height / 3, 'Info'),
    ]
    
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