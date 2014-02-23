'''
Display

'''
import libtcodpy as libtcod

class Display :

  def __init__(self, width, height) :
    libtcod.console_set_custom_font(b'terminal12x12_gs_ro.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_init_root(width, height, b'title', False, libtcod.RENDERER_GLSL)
    
    #self._selection = libtcod.console_new(1,1)
    #libtcod.console_set_default_background(self._selection, libtcod.green)
    #libtcod.console_set_background_flag(self._selection, libtcod.BKGND_LIGHTEN)
    

  def render(self, gui) :
    
    cells = gui.board.getCells()
    selected = gui.getSelected()
    
    print "SEL: ", selected
    
    for c in cells:
      for _x in range(3) :
        # Our actual position on the screen
        y = 1 + (c.y)
        x = 1 + (3 * c.x + _x)
        libtcod.console_set_char_background(0, x, y, getattr(libtcod, c.color))
        
        if selected[0] == c.x and selected[1] == c.y :
          print "Rendering selection at: ", c.x, c.y
          libtcod.console_set_char_background(0, x, y, libtcod.green, libtcod.BKGND_ADDALPHA(0.4))
          #libtcod.console_blit(self._selection, 0,0, 1,1, 0, x,y)
          
    
    
    
    libtcod.console_flush()

