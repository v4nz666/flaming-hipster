'''
Display

'''
import libtcodpy as libtcod
import frame as frame

class Display :

  def __init__(self, width, height) :
    libtcod.console_set_custom_font(b'terminal12x12_gs_ro.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_init_root(width, height, b'title', False, libtcod.RENDERER_GLSL)
    

  def render(self, gui) :
    
    for f in gui.frames:
      f.render(libtcod.magenta, libtcod.white)
    
    cells = gui.board.getCells()
    selected = gui.getSelected()
    
    
    # Draw each cell...
    for c in cells:
      # 3 Horizontal screen poisitions, per cell
      #for _x in range(3) :
        
        # Our actual position on the screen, offset by 1 for the frame...
        y = 1 + c.y
        #x = 1 + (3 * c.x + _x)
        x = 1 + c.x
        libtcod.console_set_char_background(0, x, y, getattr(libtcod, c.color))
        
        # If we're rendering the selected cell, add our selector's color
        if selected[0] == c.x and selected[1] == c.y :
          libtcod.console_set_char_background(0, x, y, libtcod.green, libtcod.BKGND_ADDALPHA(0.4))
    
    # finally, flush the console...
    libtcod.console_flush()

