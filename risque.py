'''
Documentation, License etc.

@package risque
'''
import libtcodpy as libtcod
import display as disp
import input as inp
import board as board
import gui as gui

BOARD_HEIGHT = 64
BOARD_WIDTH = 96

UI_WIDTH = 32

CONSOLE_WIDTH = 3 + BOARD_WIDTH + UI_WIDTH
CONSOLE_HEIGHT = 2 + BOARD_HEIGHT


print "Console size" + str(CONSOLE_WIDTH) + "," + str(CONSOLE_HEIGHT)

'''
Main

'''
_board = board.Board(BOARD_WIDTH, BOARD_HEIGHT)
_gui = gui.Gui(_board, UI_WIDTH)

disp = disp.Display(CONSOLE_WIDTH, CONSOLE_HEIGHT)

while not libtcod.console_is_window_closed() :
  disp.render(_gui)
  exit = inp.handleKeys(_gui)
  if exit :
    break
