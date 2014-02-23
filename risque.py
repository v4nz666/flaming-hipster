'''
Documentation, License etc.

@package risque
'''
import libtcodpy as libtcod
import display as disp
import input as inp
import board as board
import gui as gui

BOARD_WIDTH = 32
BOARD_HEIGHT = 48

CONSOLE_WIDTH = 2 + (BOARD_WIDTH * 3)
CONSOLE_HEIGHT = 2 + BOARD_HEIGHT


print "Console size" + str(CONSOLE_WIDTH) + "," + str(CONSOLE_HEIGHT)

'''
Main

'''
_board = board.Board(BOARD_WIDTH, BOARD_HEIGHT)
_gui = gui.Gui(_board)

disp = disp.Display(CONSOLE_WIDTH, CONSOLE_HEIGHT)

while not libtcod.console_is_window_closed() :
  disp.render(_gui)
  exit = inp.handleKeys(_gui)
  if exit :
    break
