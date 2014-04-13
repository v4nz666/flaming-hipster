from item import Item

class Rope(Item):
  def __init__(self, x, y):
      self.coords = [(x,y)]
      pass
  def add(self,x,y):
    if not (x, y) in self.coords:
      self.coords.append((x, y))