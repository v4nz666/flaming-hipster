from state import State
import libtcodpy as libtcod
import world as world
import gui as gui
import input as input


class GenerateWorld(State):
  def __init__(self, disp, width, height):
    State.__init__(self, disp)
    
    self.initWorld(width, height)
    self.initGui()
    
    self.registerInputHandlers()
    self.update()
  
  def refresh(self) :
    self._world.resetMap()
  
  def registerInputHandlers(self) :
    self.inputHandler = input.BlockingKeyboardHandler()
    self.inputHandler.initInputs(
      {
        'quit': {
          'key':libtcod.KEY_ESCAPE,
          'ch': None,
          'fn': self.quitToMenu
        },
        'play': {
          'key': None,
          'ch': 'p',
          'fn': self.proceed
        },
        'refresh': {
          'key': None,
          'ch': 'r',
          'fn': self.refresh
        },
        'selUp': {
          'key': libtcod.KEY_UP,
          'ch': None,
          'fn': self.selectionUp
        },
        'selDn': {
          'key': libtcod.KEY_DOWN,
          'ch': None,
          'fn': self.selectionDn
        },
        'selRgt': {
          'key': libtcod.KEY_LEFT,
          'ch': None,
          'fn': self.selectionLft
        },
        'selLft': {
          'key': libtcod.KEY_RIGHT,
          'ch': None,
          'fn': self.selectionRgt
        }
      }
    )
  
  def initWorld(self, width, height) :
    self._world = world.World(width, height)
  
  def initGui(self) :
    self._gui = gui.Gui(self.console)
    
    infoWidth = libtcod.console_get_width(self.console) - (3 + self._world.width)
    infoHeight = 10 #libtcod.console_get_height(self.console)
    
    #Our list of frames
    self._gui.addFrame(0,0,self._world.width, libtcod.console_get_height(self.console) - 2, 'Game Board')
    self._gui.addFrame(self._world.width + 1,0,infoWidth,infoHeight,'Info')
      
    self.selectedX = 0;
    self.selectedY = 0;
  
  
  
  def tick(self):
    self.update()
    return self
  
  def update(self):
    
    self.updateMessages()
    self._gui.render()
    
    #TODO Move this world-drawing bit somewhere it can be used by other states
    cells = self._world.getCells()
    
    selected = self.getSelected()
    self._world.render(self.console);
    
    for c in self._world.getCells():
      # If we're rendering the selected cell, add our selector's color
        if selected[0] == c.x and selected[1] == c.y :
          x = c.x + 1
          y = c.y + 1
          
          libtcod.console_set_char_background(self.console, x, y, libtcod.green, libtcod.BKGND_ADDALPHA(0.4))

  
  def updateMessages(self) :
    self._gui.frames['Info'].addMessage("Position : "  + str(self.getSelected()), 2 )
  
  def getSelected(self) :
    return (self.selectedX, self.selectedY)
  
  
  ######################################
  ### Key handlers
  ######################################
  def selectionUp(self) :
    y = self.selectedY - 1;
    if y >= 0 :
      self.selectedY = y
  
  def selectionDn(self) :
    y = self.selectedY + 1;
    if y < self._world.height :
      self.selectedY = y
  
  def selectionLft(self) :
    x = self.selectedX - 1;
    if x >= 0 :
      self.selectedX = x
  
  def selectionRgt(self) :
    x = self.selectedX + 1;
    if x < self._world.width :
      self.selectedX = x


  ### State transitions
  def quitToMenu(self) :
    print("Quiting!")
    self.nextState = self._states['quit']
  def proceed(self) :
    print("Proceeding!")
    self._states['play'].setWorld(self._world)
    self.nextState = self._states['play']