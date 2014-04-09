'''
Display

'''
import libtcodpy as libtcod
import frame as frame

class Display :

  def __init__(self, width, height) :
    self.width = width
    self.height = height
    libtcod.console_set_custom_font(b'prestige10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_init_root(width, height, b'title', False, libtcod.RENDERER_GLSL)

  def render(self, state) :
    console = state.getConsole()
    libtcod.console_blit(console, 0, 0, self.width, self.height, 0, 0, 0)
    libtcod.console_flush()
    
  def clear(self):
    libtcod.console_clear(0)