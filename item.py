class Item():
  def __init__(self, name, char, color):
    self.name = name
    self.char = char
    self.color = color
    self.affectedByGravity = True
    
    self.collectible = True
    self.collectedAttribute = None
    self.keepInInventory = False
    
  def setOptions(self, options):
    for k in options:
      value = options[k]
      setattr(self, k, value)