'''
input module

'''
import libtcodpy as libtcod

def handleKeys(gui) :
  key = libtcod.console_wait_for_keypress(True)
  #if key.vk == libtcod.KEY_ENTER and key.lalt:
      ##Alt+Enter: toggle fullscreen
      #libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

  if key.vk == libtcod.KEY_ESCAPE:
    return True  #exit game
  
  elif key.vk == libtcod.KEY_UP:
    gui.selectionUp()
  elif key.vk == libtcod.KEY_DOWN:
    gui.selectionDn()
  elif key.vk == libtcod.KEY_LEFT:
    gui.selectionLft()
  elif key.vk == libtcod.KEY_RIGHT:
    gui.selectionRgt()
  
  print gui.getSelected()

