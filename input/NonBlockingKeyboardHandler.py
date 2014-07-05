import libtcodpy as libtcod
from KeyboardHandler import KeyboardHandler

class NonBlockingKeyboardHandler(KeyboardHandler):
  
  gotInput = False
  
  def handleInput(self):
    
    key = libtcod.console_check_for_keypress()
    if key.vk != libtcod.KEY_NONE:
      self.handleKeyInput(key)
      self.gotInput = True
    else:
      self.gotInput = False