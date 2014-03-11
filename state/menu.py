import state
import subState
import libtcodpy as libtcod

class Menu(state.State):
  def __init__(self, name):
    state.State.__init__(self, name)
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
        'subStateTransition': {
          'key': None,
          'ch': 's',
          'fn': self.sub
        }
      }
    )
  def refresh(self) :
    print("Refresh!!")
    return self
  def quit(self) :
    print("Quiting!")
    return False
  
  def sub(self):
    print("transitioning")
    sub = subState.subState('Sub Menu')
    while sub.tick():
      pass
    return self
  
  
  def tick(self):
    key = libtcod.console_wait_for_keypress(True)
    return self.handleInput(key)
