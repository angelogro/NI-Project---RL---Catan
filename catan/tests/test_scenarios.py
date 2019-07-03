import numpy as np

def test_initial_placement():
    # set tiles 6,6,8,8 close or next to each other
    # to collect highest amount of cards
    # just collecting random cards -maybe for reward = "cards"
    tiles = [(0, 6), (4, 8), (0, 9),
               (3, 8), (4, 6), (1, 12), (1, 4),
               (1, 9), (3, 2), (5, 7), (2, 5), (1, 10),
               (4, 3), (2, 5), (3, 10), (4, 11),
               (0, 3), (0, 4), (2, 11)]

    optimal_crossings = [0, 1, 2, 3, 4,
                         7, 8, 9, 10, 11,
                         17, 18, 19, 20, 21]
    # look for optimal crossings - Data rep # define function for counting how often placed in optimal place
    # define tiles in order to collect materials good for settlement building
    # define tiles in order to collect materials good for city building
    return tiles, optimal_crossings
    # count how often placed on crossings connected to tiles with highest prob to collect resources


def one_settlement():
    # giving enough resources to build one settlement and a road
    return np.array([1, 1, 0, 2, 2])


def test_city():
    return np.array([2, 0, 3, 0, 0])

