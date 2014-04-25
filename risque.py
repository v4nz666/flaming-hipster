'''
Documentation, License etc.

@package risque
'''
import libtcodpy as libtcod
import display as disp
import input as inp
import sys
import state

WIN_MAIN_WIDTH = 32
WIN_MAIN_HEIGHT = 48
WIN_RIGHT_WIDTH = 32

WORLD_HEIGHT = WIN_MAIN_HEIGHT * 5

CONSOLE_WIDTH = 3 + WIN_MAIN_WIDTH + WIN_RIGHT_WIDTH
CONSOLE_HEIGHT = 2 + WIN_MAIN_HEIGHT

disp = disp.Display(CONSOLE_WIDTH, CONSOLE_HEIGHT)

s_Menu = state.Menu(disp)
s_WorldGen = state.GenerateWorld(disp, WIN_MAIN_WIDTH, WORLD_HEIGHT)
s_Play = state.Play(disp)
s_Death = state.Death(disp)
s_Quit = state.Quit(disp)

states = {
  'quit': s_Quit,
  'menu': s_Menu,
  'generate': s_WorldGen,
  'play': s_Play,
  'death': s_Death
}


for (name, state) in states.items():
  state.registerStates(states)

'''
Main

'''
currentState = s_WorldGen
while not libtcod.console_is_window_closed() :

  disp.render(currentState)
  currentState.inputHandler.handleInput()
  currentState.tick()
  newState = currentState.nextState
  
  if newState != currentState:
    currentState.reset()
    currentState = newState
    currentState.beforeTransition()
    disp.clear()
  