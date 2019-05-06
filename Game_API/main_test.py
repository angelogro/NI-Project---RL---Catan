from Game import *

def test_road_build_possibilities():
    g = Game(random_init=True)
    g.place_settlement(8,1)
    g.place_road(12,1)
    g.place_road(13,1)
    g.place_road(14,1)

    g.place_road(7,3)
    g.place_road(6,3)


    p3_roads = g.roads.get_possible_actions_build_road(3)
    assert sum(p3_roads) == 4

    p2_roads = g.roads.get_possible_actions_build_road(2)
    assert sum(p2_roads) == 0

    p1_roads = g.roads.get_possible_actions_build_road(1)
    assert sum(p1_roads) == 6

test_road_build_possibilities()