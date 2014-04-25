from state import State
import libtcodpy as libtcod
import time
import gui as gui
import input as input

class Death(State):
  def __init__(self, disp):
    State.__init__(self, disp)
    self.initGui()
    self.registerInputHandlers()
    self.frameCount = 0;
    self.done = False
    
  
  def registerInputHandlers(self) :
    self.inputHandler = input.NonBlockingKeyboardHandler()
    self.inputHandler.initInputs(
      {
        'proceed': {
          'key':libtcod.KEY_ENTER,
          'ch': None,
          'fn': self.proceed
        },
      }
    )
  
  def initGui(self) :
    self._gui = gui.Gui(self.console)
    self._gui.addFrame(0,0,libtcod.console_get_width(self.console) - 1, libtcod.console_get_height(self.console), 'You have died!')
    self._gui.frames['You have died!'].setFrameColor('white')
    
  def tick(self):
    if self.done:
      time.sleep(2)
      self.nextState = self._states['generate']
      return self
    
    self.update()
    self.frameCount = self.frameCount + 1
    return self
  
  def update(self):
    self._gui.render()
    
    frame = self._gui.frames['You have died!']

    if self.frameCount <= frame.innerHeight:
      for y in range(self.frameCount):
        for x in range(frame.innerWidth + 1):
          frame.setBgColor(x, y, libtcod.darker_red, libtcod.BKGND_SET)
    else:
      self.done = True
      self._gui.frames['You have died!'].addMessage("You have died.", 3)
      self._gui.frames['You have died!'].addMessage("Better luck next time", 5)
      self._gui.render()

    
  
  ######################################
  ### Key handlers
  ######################################

  def proceed(self) :
    self.nextState = self._states['generate']
