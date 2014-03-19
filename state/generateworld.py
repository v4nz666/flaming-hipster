from state import State
import libtcodpy as libtcod
import world as world
import gui as gui

class GenerateWorld(State):
  def __init__(self, width, height):
    State.__init__(self)
    self.initWorld(width, height)
    self.initInputs(
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
  
  def refresh(self) :
    self._world.resetMap()
  
  def quit(self) :
    print("Quiting!")
    return False
  
  def initWorld(self, width, height) :
    self._world = world.World(width, height)
    self._gui = gui.Gui(self._world, width)
  
  
  
  
  
  def tick(self) :
    key = libtcod.console_wait_for_keypress(True)
    if self.handleInput(key) == False:
      return False
    else:
      return self
  