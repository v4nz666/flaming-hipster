class Item():
  def __init__(self, name, char, color):
    self.name = name
    self.char = char
    self.color = color
    self.collectible = True
    self.affectedByGravity = True
    
  def setOptions(self, options):
    for k in options:
      value = options[k]
      setattr(self, k, value)