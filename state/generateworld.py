from state import State
import libtcodpy as libtcod
import world as world
import gui as gui
import input as input


class GenerateWorld(State):
  def __init__(self, disp, width, height):
    State.__init__(self)
    self.disp = disp
    self.console = libtcod.console_new(disp.width, disp.height)
    
    self.initWorld(width, height)
    self.inputHandler = input.BlockingKeyboardHandler()
    
    self.inputHandler.initInputs(
      {
        'quit': {
          'key':libtcod.KEY_ESCAPE,
          'ch': None,
          'fn': self.quit
        },
        'refresh': {
          'key': None,
          'ch': 'r',
          'fn': self.refresh
        },
        'selUp': {
          'key': libtcod.KEY_UP,
          'ch': None,
          'fn': self._gui.selectionUp
        },
        'selDn': {
          'key': libtcod.KEY_DOWN,
          'ch': None,
          'fn': self._gui.selectionDn
        },
        'selRgt': {
          'key': libtcod.KEY_LEFT,
          'ch': None,
          'fn': self._gui.selectionLft
        },
        'selLft': {
          'key': libtcod.KEY_RIGHT,
          'ch': None,
          'fn': self._gui.selectionRgt
        }
      }
    )
    self.update()
  
  
  def refresh(self) :
    self._world.resetMap()
  
  def quit(self) :
    print("Quiting!")
    self.nextState = self._states['quit']
  
  def initWorld(self, width, height) :
    self._world = world.World(width, height)
    self._gui = gui.Gui(self.console, self._world, width)
  
  def tick(self):
    self.update()
    return self
  
  def update(self):
    for key in self._gui.frames:
      self._gui.frames[key].renderFrame()
    
    for key in self._gui.frames:
      self._gui.frames[key].renderTitle()

    self._gui.updateMessages()
    for key in self._gui.frames:
      self._gui.frames[key].printMessages()
    
    
    cells = self._gui.board.getCells()
    selected = self._gui.getSelected()
    
    # Draw each cell...
    for c in cells:
        # Our actual position on the screen, offset by 1 for the frame...
        y = 1 + c.y
        x = 1 + c.x
        libtcod.console_set_char_background(self.console, x, y, getattr(libtcod, c.color))
        
        # If we're rendering the selected cell, add our selector's color
        if selected[0] == c.x and selected[1] == c.y :
          libtcod.console_set_char_background(self.console, x, y, libtcod.green, libtcod.BKGND_ADDALPHA(0.4))
  