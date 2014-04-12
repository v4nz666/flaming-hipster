import libtcodpy as libtcod
from KeyboardHandler import KeyboardHandler

class NonBlockingKeyboardHandler(KeyboardHandler):
  def handleInput(self):
    
    key = libtcod.console_check_for_keypress()
    if key:
      self.handleKeyInput(key)