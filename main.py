import sys
import state
import libtcodpy as libtcod

menu = state.Menu('Menu')

states = [menu]

# Do this... so states know about all available states, and can pass them back from their tick() method
for state in states :
  state.registerStates(states)


currentState = menu
  
libtcod.console_set_custom_font(b'prestige10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_set_default_foreground(0, libtcod.white)
libtcod.console_init_root(96, 64, b'State Machine', False, libtcod.RENDERER_GLSL)

while not libtcod.console_is_window_closed() :
  libtcod.console_clear(0)
  currentState = currentState.tick()
  if currentState == False:
    sys.exit()
  libtcod.console_flush()
  