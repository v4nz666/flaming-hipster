'''
Documentation, License etc.

@package risque
'''
import libtcodpy as libtcod
import display as disp
import input as inp
import sys
import state

WIN_MAIN_HEIGHT = 64
WIN_MAIN_WIDTH = 96

WIN_RIGHT_WIDTH = 32

CONSOLE_WIDTH = 3 + WIN_MAIN_WIDTH + WIN_RIGHT_WIDTH
CONSOLE_HEIGHT = 2 + WIN_MAIN_HEIGHT

s_WorldGen = state.GenerateWorld(WIN_MAIN_WIDTH, WIN_MAIN_HEIGHT)


currentState = s_WorldGen
'''
Main

'''

disp = disp.Display(CONSOLE_WIDTH, CONSOLE_HEIGHT)

while not libtcod.console_is_window_closed() :

  disp.render(currentState._gui)
  currentState = currentState.tick()
  currentState.inputHandler.handleInput()