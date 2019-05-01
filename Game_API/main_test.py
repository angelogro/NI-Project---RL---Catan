
from Game import Hex_tiles
from Game import Crossings,Roads
h = Hex_tiles(random_init=True)
c = Crossings(h.get_tiles(),h.harbours)
r = Roads(c.get_neighbouring_crossings())
print(h.get_tiles())
print(h.get_tile_state())
print(c.get_state())
print(r.get_state())
print(r.get_roads())
print(c.get_crossings())