from Game import *
import Defines
import time

def test_discard_robbed_cards_no_cards():
    g = Game(random_init=False)
    g.place_settlement(10, 1)
    g.discard_resources()
    assert sum(g.cards[0,:])==0

test_discard_robbed_cards_no_cards()

def test_discard_robbed_cards_few_cards():
    g = Game(random_init=False)
    g.place_settlement(10, 1)
    g.cards[0,:] = [1,2,2,0,1]
    g.discard_resources()
    assert sum(g.cards[0,:])==6

test_discard_robbed_cards_few_cards()

def test_discard_robbed_cards_enough_cards():
    g = Game(random_init=False)
    g.place_settlement(10, 1)
    g.cards[0,:] = [5,5,5,5,5]
    g.discard_resources()
    assert sum(g.cards[0,:])==13

test_discard_robbed_cards_enough_cards()

def test_2vs_1_trade_noresources():
    g = Game(random_init=False)
    g.place_settlement(10, 1)
    assert sum(g.get_possible_actions_trade_2vs1(1))==0

test_2vs_1_trade_noresources()

def test_2vs_1_trade_resources_no_port():
    g = Game(random_init=False)
    g.place_settlement(10, 1)
    g.cards[0,:] = [5,5,5,5,5]
    assert sum(g.get_possible_actions_trade_2vs1(1))==0

test_2vs_1_trade_resources_no_port()

def test_2vs_1_trade_noresources_but_port():
    g = Game(random_init=False)
    g.place_settlement(0, 1)
    assert sum(g.get_possible_actions_trade_2vs1(1))==0

test_2vs_1_trade_noresources_but_port()

def test_2vs_1_trade_resources_and_1port():
    g = Game(random_init=False)
    g.place_settlement(0, 1) # has ore-port
    g.cards[0,2] = 3 # has 3 ore
    assert sum(g.get_possible_actions_trade_2vs1(1))==4 # possible trade against 4 resources

test_2vs_1_trade_resources_and_1port()

def test_2vs_1_trade_resources_and_3port():
    g = Game(random_init=False)
    g.place_settlement(0, 1) # has ore-port
    g.place_city(4, 1) # has wool-port
    g.place_settlement(45, 1) # has grain-port
    g.cards[0,2] = 3 # has 3 ore
    g.cards[0,1] = 2 # has 2 wool
    g.cards[0,0] = 4 # has 2 grain
    assert sum(g.get_possible_actions_trade_2vs1(1))==12 # possible trade against 4 resources

test_2vs_1_trade_resources_and_3port()

def test_3vs_1_trade_all_resources_available():
    g = Game(random_init=False)
    g.place_settlement(27, 1) # has 3vs1 port
    g.place_settlement(19, 2) # has no port
    g.place_settlement(21, 3)
    g.place_settlement(13, 4)
    g.cards[0,0]=3 # giving the player 0 3 grain
    g.cards[0,1]=3 # giving him also 3 wool
    g.cards[0,2]=3
    g.cards[0,3]=3
    g.cards[0,4]=3

    g.cards[1,:] = np.array([3,3,3,3,3])

    g.create_possible_trade_sets_3vs1()
    s = time.time()
    possible_actions = g.get_possible_actions_trade_3vs1(1)
    e = time.time()
    print(e-s)
    assert sum(possible_actions) == 100

    possible_actions = g.get_possible_actions_trade_3vs1(2)
    assert sum(possible_actions) == 0


test_3vs_1_trade_all_resources_available()

def test_3vs_1_trade_some_resources():
    g = Game(random_init=False)
    g.place_settlement(27, 1)
    g.place_settlement(19, 2)
    g.place_settlement(21, 3)
    g.place_settlement(13, 4)
    g.cards[0,0]=1 # 1 grain
    g.cards[0,1]=1 # 1 wool
    g.cards[0,2]=1 # 1 ore

    g.create_possible_trade_sets_3vs1()
    possible_actions = g.get_possible_actions_trade_3vs1(1)
    # Should only be possible to trade against wood and brick...
    assert sum(possible_actions) == 2
    g.cards[0,2]=0 # 1 ore
    possible_actions = g.get_possible_actions_trade_3vs1(1)
    assert sum(possible_actions) == 0
test_3vs_1_trade_some_resources()

def test_rob():
    g = Game(random_init=False)
    g.place_settlement(10, 1)
    g.place_settlement(19, 2)
    g.place_settlement(21, 3)
    g.place_settlement(13, 4)
    g.cards[1,0] = 1 #give player 1 one grain
    g.set_robber_position(4)
	
    print("Robber State " ,g.get_robber_state())

    print("Building state ", g.building_state)
    print("Robable players ", g.get_possible_actions_rob_player(1))
    print("Robable players ", g.rob_person(1))

test_rob()






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

    #Testing if roads can be placed at the correct places
    np.testing.assert_array_equal(g.get_possible_actions_build_road(1,init_state=True),possible_roadarray)

#test_init_placing()

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

    assert sum(g.get_possible_actions_build_settlement(2))==2
    assert sum(g.get_possible_actions_build_settlement(1))==1

#test_settlement_placing()


def test_city_placing():
    g = Game(random_init=True)
    g.place_settlement(10,1)
    g.place_settlement(14,2)
    g.place_settlement(34,2)
    g.place_settlement(20,2)
    g.place_settlement(17,1)
    g.place_road(9,2)
    g.place_road(8,2)
    g.place_road(6,2)
    g.place_road(4,1)
    g.place_road(13,1)
    g.place_road(15,1)
    g.place_road(17,1)


    possible_crossings = np.array([10,17])
    possible_array = np.zeros(Defines.NUM_CROSSINGS)
    possible_array[possible_crossings] = 1

    np.testing.assert_array_equal(g.get_possible_actions_build_city(1),possible_array)

    possible_crossings = np.array([14,20,34])
    possible_array = np.zeros(Defines.NUM_CROSSINGS)
    possible_array[possible_crossings] = 1

    np.testing.assert_array_equal(g.get_possible_actions_build_city(2),possible_array)

#test_city_placing()


def test_develop_one_player():
    # Using the initial fixed setup
    g = Game(random_init=False)

    # Putting settlement and roads to places so that all resources are accessible
    g.place_settlement(42,1)
    g.place_settlement(35,1)
    g.place_settlement(19,1)
    g.place_road(36,1)
    g.place_road(38,1)
    g.place_road(14,1)

    # Iterate some turns for player and letting it sample randomly from all possible actions
    for i in range(10):
        g.roll_dice() # automatically distributes resources
        print(g.get_possible_actions_build_road(1)*1)
        actions = g.get_possible_actions(1)
        if sum(actions)>=1:
            chosen_action = np.random.choice(len(actions), 1, p=actions/sum(actions))
            g.take_action(chosen_action[0],1)

    print("From test_develop_one_player() :" )
    print(g.cards)
    print(g.building_state)
    print(g.roads.get_state())

#test_develop_one_player()

def test_develop_two_player():
    # Using the initial fixed setup
    g = Game(random_init=False)

    # Putting settlement and roads to places so that all resources are accessible
    g.place_settlement(42,1)
    g.place_settlement(35,1)

    g.place_road(36,1)
    g.place_road(38,1)

    g.place_settlement(40,2)
    g.place_settlement(13,2)

    g.place_road(18,2)
    g.place_road(44,2)


    # Iterate some turns for player and letting it sample randomly from all possible actions
    for i in range(20):
        g.current_player = 1 if g.current_player == 2 else 2
        g.roll_dice() # automatically distributes resources
        actions = g.get_possible_actions(g.current_player)
        if sum(actions)>=1:
            chosen_action = np.random.choice(len(actions), 1, p=actions/sum(actions))
            g.take_action(chosen_action[0],g.current_player)

    # As player 2 is intially worsely placed than player 1 we expect him to have fewer buildings and resources
    print("From test_develop_two_player() :" )
    print(g.cards)
    print(g.building_state)
    print(g.roads.get_state())

#test_develop_two_player()

