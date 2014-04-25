'''
Frame

'''
import libtcodpy as libtcod

class Frame:
  
  x = y = 0
  w = h = 0
  ch = '#'
  
  colFrame = libtcod.white
  colText = libtcod.white
  
  def __init__(self, console, x, y, w, h, name):
    
    self.console = console
    
    #x, y coordinates, on screen
    self.x = x
    self.y = y
    
    #total width and height, including border
    self.w = w
    self.h = h
    
    #number of inner rows
    self.innerHeight = h - 2
    #number of inner columns
    self.innerWidth = w - 2
    
    self.name = name
    
    self.setTextColor(b'white');
    self.setFrameColor(b'light_blue');
    
    self.messages = [None for y in range(self.h)]
    
  
  def putChar(self, x, y, char, col):
    x = x + self.x + 1
    y = y + self.y + 1
    libtcod.console_put_char(self.console, x, y, char)
    libtcod.console_set_char_foreground(self.console, x, y, getattr(libtcod, col))
  
  def setBgColor(self, x, y, col, flag):
    screenX = x + self.x + 1
    screenY = y + self.y + 1
    
    if isinstance(col, type(b'')):
      col = getattr(libtcod, col)
    
    libtcod.console_set_char_background(self.console, screenX, screenY, col, flag)
  
  def addMessage(self, str, pos) :
    self.messages[pos] = str
  
  def printMessages(self) :
    for pos, msg in enumerate(self.messages) :
      if msg != None:
        self.printMsg(pos, msg)
  
  def printMsg(self, y, msg) :
    for k, c in enumerate(msg) :
      if k >= self.w :
        break
      x = 1 + self.x + k
      _y = self.y + y
      libtcod.console_put_char(self.console, x, _y, c)
      libtcod.console_set_char_foreground(self.console, x, _y, self.colText)
    
  def setTextColor(self, col) :
    self.colText = getattr(libtcod, col)
    
  def setFrameColor(self, col) :
    self.colFrame= getattr(libtcod, col)
    
  def renderFrame(self) :
    for i in range (self.w + 1) :
      
      x = self.x + i
      y1 = self.y
      y2 = self.y + self.h - 1
      
      libtcod.console_put_char(self.console, x, y1, self.ch)
      libtcod.console_put_char(self.console, x, y2, self.ch)
      
      libtcod.console_set_char_foreground(self.console, x, y1, self.colFrame)
      libtcod.console_set_char_foreground(self.console, x, y2, self.colFrame)
    
    #we've already drawn the corners
    for j in range (1, self.h) :
      
      y = self.y + j
      x1 = self.x
      x2 = self.x + self.w
      
      libtcod.console_put_char(self.console, x1, y, self.ch)
      libtcod.console_put_char(self.console, x2, y, self.ch)
    
      libtcod.console_set_char_foreground(self.console, x1, y, self.colFrame)
      libtcod.console_set_char_foreground(self.console, x2, y, self.colFrame)
    
  def renderTitle(self) :
    
    self.printMsg(0, self.name)
    