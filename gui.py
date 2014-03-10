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
    self.frames = {
      'main': frame.Frame(0,0,board.width,board.height, 'Game Board'),
      'info': frame.Frame(board.width + 1,0, uiWidth, board.height, 'Info'),
    }
    
    for key in self.frames :
      self.frames[key].setTextColor('white');
      self.frames[key].setFrameColor('light_blue');
    
    return
  
  def updateMessages(self) :
    self.frames['info'].addMessage("Position : "  + str(self.getSelected()), 2 )
  
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