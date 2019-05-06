from Game import *
from Game import Hex_tiles
from Game import Crossings,Roads
g = Game(random_init=True)


g.roll_dice()
g.roll_dice()
g.roll_dice()

conns = g.roads.get_roads()
r_s = g.roads.get_state()

print(conns[r_s==1])

print(np.unique(conns[r_s==2]))

crossings_connected = g.get_possible_actions_build_settlement(1)
print(crossings_connected)