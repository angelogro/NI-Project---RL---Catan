from Game import *
import Defines

def test_road_build_possibilities():
    g = Game(random_init=True)
    g.place_settlement(8,1)
    g.place_road(12,1)
    g.place_road(13,1)
    g.place_road(14,1)

    g.place_road(7,3)
    g.place_road(6,3)


    p3_roads = g.get_possible_actions_build_road(3)
    assert sum(p3_roads) == 4

    p2_roads = g.get_possible_actions_build_road(2)
    assert sum(p2_roads) == 0

    p1_roads = g.get_possible_actions_build_road(1)
    assert sum(p1_roads) == 6

#test_road_build_possibilities()

def test_init_placing():
    g = Game(random_init=True)
    g.crossings.create_connected_roads(g.roads.get_roads())
    g.place_settlement(10,1)
    g.place_settlement(14,2)
    g.place_road(9,2)

    possible_crossings = np.array([2,9,11,6,13,15,10,14])
    possible_array = np.ones(Defines.NUM_CROSSINGS)
    possible_array[possible_crossings] = 0

    # This replaces assert for numpy arrays
    np.testing.assert_array_equal(g.get_possible_actions_build_settlement(3,init_state=True),possible_array)

    possible_road_indices = np.array([4,13,15])
    possible_roadarray = np.zeros(Defines.NUM_EDGES)
    possible_roadarray[possible_road_indices] = 1


    print(g.roads.get_roads())
    #Testing if roads can be placed at the correct places
    np.testing.assert_equal(g.get_possible_actions_build_road(1,init_state=True),possible_roadarray)

test_init_placing()

def test_settlement_placing():
    g = Game(random_init=True)
    g.place_settlement(10,1)
    g.place_settlement(14,2)
    g.place_road(9,2)
    g.place_road(8,2)
    g.place_road(6,2)
    g.place_road(4,1)
    g.place_road(13,1)
    g.place_road(15,1)
    g.place_road(17,1)

    print(g.get_possible_actions_build_settlement(2))
    print(g.get_possible_actions_build_settlement(1))
    assert sum(g.get_possible_actions_build_settlement(2))==2
    assert sum(g.get_possible_actions_build_settlement(1))==1

#test_settlement_placing()

g = Game(random_init=True)
g.place_settlement(10,1)
g.place_settlement(8,1)
g.place_road(10,1)
g.place_settlement(14,2)
g.place_road(9,2)

print(g.roads.get_roads())
print(g.roads.get_state())
print(g.crossings.get_building_state())

g.get_possible_actions_build_road(1,init_state=True)

