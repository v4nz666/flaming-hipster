import libtcodpy as libtcod
from KeyboardHandler import KeyboardHandler

class BlockingKeyboardHandler(KeyboardHandler):
  def handleInput(self):
    key = libtcod.console_wait_for_keypress(True)
    self.handleKeyInput(key)