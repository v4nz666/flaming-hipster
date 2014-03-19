import state
import libtcodpy as libtcod

class subState(state.State):
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
        }
      }
    )
  def refresh(self) :
    print("Sub Refresh!!")
    return self
  def quit(self) :
    print("Sub Quiting!")
    return False
    
  def tick(self):
    key = libtcod.console_wait_for_keypress(True)
    return self.handleInput(key)