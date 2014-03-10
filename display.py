'''
Display

'''
import libtcodpy as libtcod
import frame as frame

class Display :

  def __init__(self, width, height) :
    #libtcod.console_set_custom_font(b'terminal12x12_gs_ro.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_set_custom_font(b'prestige10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_init_root(width, height, b'title', False, libtcod.RENDERER_GLSL)
    

  def render(self, gui) :
    
    libtcod.console_clear(0)
    for key in gui.frames:
      gui.frames[key].renderFrame()
    
    for key in gui.frames:
      gui.frames[key].renderTitle()

    gui.updateMessages()
    for key in gui.frames:
      gui.frames[key].printMessages()
    
    
    cells = gui.board.getCells()
    selected = gui.getSelected()
    
    
    # Draw each cell...
    for c in cells:
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

