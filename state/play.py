
'''
Play State
'''
from state import State
import input as input
import libtcodpy as libtcod
import gui as gui
import player as player

class Play(State):
  #TODO optional parameter for disp? not used here...
  def __init__(self, disp):
    State.__init__(self,disp)
    self.inputHandler = input.NonBlockingKeyboardHandler()
    self.inputHandler.initInputs(
      {
        'quit': {
          'key':libtcod.KEY_ESCAPE,
          'ch': None,
          'fn': self.quitToMenu
        },
          'mvUp': {
          'key': libtcod.KEY_UP,
          'ch': None,
          'fn': self.mvUp
        },
        'mvDn': {
          'key': libtcod.KEY_DOWN,
          'ch': None,
          'fn': self.mvDn
        },
        'mvRgt': {
          'key': libtcod.KEY_LEFT,
          'ch': None,
          'fn': self.mvLft
        },
        'mvLft': {
          'key': libtcod.KEY_RIGHT,
          'ch': None,
          'fn': self.mvRgt
        }
    }
    )
    
  
  def beforeTransition(self):
    self.initGui()
    
  def initGui(self) :
    self._gui = gui.Gui(self.console)
    
    infoWidth = libtcod.console_get_width(self.console) - (3 + self._world.width)
    infoHeight = 10
    
    #Our list of frames
    self._gui.addFrame(0,0,self._world.width, libtcod.console_get_height(self.console) - 2, 'Game Board')
    self._gui.addFrame(self._world.width + 1,0,infoWidth,infoHeight,'Info')
    
    self.update()
    
  def setWorld(self, world):
    self._world = world
    self.initFovMap()
    
    #TODO this shouldn't be here
    self.player = player.Player(0,0, self._world)
  
  def tick(self):
    self.update()
    return
  
  def update(self):
    
    libtcod.console_clear(self.console)
    self.updateMessages()
    self._gui.render()
    #self._world.render(self.console)
    self.player.render(self.console)
    

  def initFovMap(self):
    for x in range(self._world.width):
      for y in range(self._world.height):
        c = self._world.getCell(x,y)
        libtcod.map_set_properties(self._world.map, x, y, c.passable, c.passable)
  
  def updateMessages(self) :
    self._gui.frames['Info'].addMessage("Position : " + str((self.player.x, self.player.y)), 2 )


  ######################################
  ### Key handlers
  ######################################
  def mvUp(self) :
    y = self.player.y - 1;
    cell = self._world.getCell(self.player.x, y)
    if y >= 0 and cell.passable:
      self.player.y = y
  
  def mvDn(self) :
    y = self.player.y + 1;
    cell = self._world.getCell(self.player.x, y)
    if y < self._world.height and cell.passable:
      self.player.y = y
  
  def mvLft(self) :
    x = self.player.x - 1;
    cell = self._world.getCell(x, self.player.y)
    if x >= 0 and cell.passable:
      self.player.x = x
  
  def mvRgt(self) :
    x = self.player.x + 1;
    cell = self._world.getCell(x, self.player.y)
    if x < self._world.width and cell.passable:
      self.player.x = x









  def quitToMenu(self) :
    #self.nextState = self._states['menu']
    self.nextState = self._states['generate']