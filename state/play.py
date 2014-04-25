
'''
Play State
'''
from state import State
import input as input
import libtcodpy as libtcod
import gui as gui
import player as player

class Play(State):
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
          'key': libtcod.KEY_KP8,
          'ch': None,
          'fn': self.mvUp
        },
        'mvDn': {
          'key': libtcod.KEY_KP2,
          'ch': None,
          'fn': self.mvDn
        },
        'mvRgt': {
          'key': libtcod.KEY_KP6,
          'ch': None,
          'fn': self.mvRgt
        },
        'mvLft': {
          'key': libtcod.KEY_KP4,
          'ch': None,
          'fn': self.mvLft
        },
        'mvUpLft': {
          'key': libtcod.KEY_KP7,
          'ch': None,
          'fn': self.mvUpLft
        },
        'mvUpRgt': {
          'key': libtcod.KEY_KP9,
          'ch': None,
          'fn': self.mvUpRgt
        },
        'mvDnLft': {
          'key': libtcod.KEY_KP1,
          'ch': None,
          'fn': self.mvDnLft
        },
        'mvDnRgt': {
          'key': libtcod.KEY_KP3,
          'ch': None,
          'fn': self.mvDnRgt
        },
        
        'toggleRope': {
          'key': libtcod.KEY_SPACE,
          'ch': None,
          'fn': self.ropeToggle
        }
    })
    
    self.calculateFov = True
    
    # End: __init__
  
  def beforeTransition(self):
    self.player = player.Player(0,0, self._world)
    self.initGui()
    self.update()
    self.calculateFov = True

  def initGui(self) :
    self._gui = gui.Gui(self.console)
    
    infoWidth = libtcod.console_get_width(self.console) - (2 + self._world.width)
    infoHeight = 10
    
    #Our list of frames
    self._gui.addFrame(0,0,self._world.width + 1, libtcod.console_get_height(self.console), 'Main')
    self._gui.addFrame(self._world.width + 1,0,infoWidth,infoHeight,'Info')
  
  def setWorld(self, world):
    self._world = world
    self.initFovMap()
  
  def tick(self):
    self.update()
    return
  
  def update(self):
    libtcod.console_clear(self.console)
    if self.calculateFov:
      self.calculateFov = False
      libtcod.map_compute_fov(
        self._world.map, self.player.x, self.player.y, self.player.torchStrength, True, libtcod.FOV_SHADOW)
    
    self.updateMessages()
    self._gui.render()
    self._world.render(self._gui.frames['Main'], 0)
    self.player.render(self.console)
    try:
      if not self.player.anchored:
        cellBelow = self._world.getCell(self.player.x, self.player.y + 1)
        if cellBelow.passable:
          self.calculateFov = True
          self.player.mvDn()
    except:
      pass
    self.player.update()

  def initFovMap(self):
    for x in range(self._world.width):
      for y in range(self._world.height):
        c = self._world.getCell(x,y)
        libtcod.map_set_properties(self._world.map, x, y, c.passable, c.passable)
  
  def updateMessages(self) :
    self._gui.frames['Info'].addMessage("Position : " + str((self.player.x, self.player.y)), 2 )
    self._gui.frames['Info'].addMessage("Anchors  : " + str(self.player.anchors), 3 )
    self._gui.frames['Info'].addMessage("Ropes    : " + str(self.player.ropes), 4 )
    self._gui.frames['Info'].addMessage("Clipped  : " + str(len(self.player.clippedRopes)), 5 )

  ######################################
  ### Key handlers
  ######################################
  def mvUp(self) :
    y = self.player.y - 1;
    cell = self._world.getCell(self.player.x, y)
    if y >= 0 and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvUp()
  
  def mvDn(self) :
    y = self.player.y + 1;
    cell = self._world.getCell(self.player.x, y)
    if y < self._world.height and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvDn()
  
  def mvLft(self) :
    x = self.player.x - 1;
    cell = self._world.getCell(x, self.player.y)
    if x >= 0 and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvLt()
  
  def mvRgt(self) :
    x = self.player.x + 1;
    cell = self._world.getCell(x, self.player.y)
    if x < self._world.width and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvRt()
    

  def mvUpLft(self) :
    y = self.player.y - 1
    x = self.player.x - 1
    cell = self._world.getCell(x, y)
    if y >= 0 and x >= 0 and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvUpLft()
  
  def mvUpRgt(self) :
    y = self.player.y - 1
    x = self.player.x + 1
    cell = self._world.getCell(x, y)
    if y >= 0 and x < self._world.width  and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvUpRgt()
  
  def mvDnLft(self) :
    y = self.player.y + 1
    x = self.player.x - 1
    cell = self._world.getCell(x, y)
    if y < self._world.height and x >= 0 and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvDnLft()
  
  def mvDnRgt(self) :
    y = self.player.y + 1
    x = self.player.x + 1
    cell = self._world.getCell(x, y)
    if y < self._world.height and x < self._world.width and ( 
        cell.passable or self._world.dig(cell.x, cell.y, self.player) ):
      self.calculateFov = True
      self.player.mvDnRgt()
  
  def ropeToggle(self):
    if self.player.anchored:
      self.player.detach()
    else:
      self.player.anchorRope()
    
  ##############################################
  ### State transitions

  def quitToMenu(self) :
    #self.nextState = self._states['menu']
    self.nextState = self._states['generate']