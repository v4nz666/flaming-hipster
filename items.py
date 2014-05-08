from item import Item

class Items():
  Anchor = Item('Anchor', '"', b'lightest_grey')
  Anchor.setOptions({
    'collectible': False,
    'affectedByGravity': False
  })
  Water = Item('Water', '~', b'light_blue')
  Water.setOptions({
    'affectedByGravity': False,
    'collectedAttribute': ['health', 10]
  })
  Iron = Item('Iron', '*', b'silver')
  Iron.setOptions({
    'affectedByGravity': True,
    'collectedAttribute': ['pickAxe', 10]
  })
  Coal = Item('Coal', '*', b'black')
  Coal.setOptions({
    'affectedByGravity': True,
  })
  