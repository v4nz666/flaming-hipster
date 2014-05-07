from item import Item

class Items():
  Anchor = Item('Anchor', '"', b'lightest_grey')
  Anchor.setOptions({
    'collectible': False,
    'affectedByGravity': False
  })
  Water = Item('Water', '~', b'light_blue')
  Water.setOptions({
    'affectedByGravity': False
  })
  Iron = Item('Iron', '+', b'silver')
  Iron.setOptions({
    'affectedByGravity': True
  })
  