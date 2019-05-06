import random

import numpy as np
from scipy.sparse import coo_matrix
import Defines



class Crossings:
    def __init__(self,tiles,harbours):
        """
        Intializes the crossing variables.

        """
        # Indices of neighbouring crossings
        self.neighbouring_crossings=[[1, 8], [2, 0], [3, 1, 10], [4, 2], [5, 3, 12], [6, 4], [5, 14],
                                     [8,17],[0,7,9],[8,10,19],[2,9,11],[10,12,21],[4,11,13],[12,14,23],[13,15,6],[14,25],
                                     [17,27],[16,7,18],[17,29,19],[18,9,20],[19,31,21],[20,11,22],[21,23,33],[22,13,24],[23,25,35],[24,15,26],[25,37],
                                     [16,28],[27,29,38],[28,18,30],[29,31,40],[30,20,32],[31,33,42],[32,22,34],[33,35,44],[34,36,24],[35,37,46],[26,36],
                                     [28,39],[38,40,47],[39,30,41],[40,42,49],[41,32,43],[42,44,51],[43,34,45],[44,53,46],[36,45],
                                     [39,48],[47,49],[48,41,50],[49,51],[50,43,52],[51,53],[52,45]]
        # Indices of neighbouring tiles
        self.neighbouring_tiles=[[0],[0],[0,1],[1],[1,2],[2],[2],
                                 [3],[0,3],[3,4],[0,1,4],[1,4,5],[1,2,5],[2,5,6],[2,6],[6],
                                 [7],[3,7],[3,7,8],[3,4,8],[4,8,9],[4,5,9],[5,9,10],[5,6,10],[6,10,11],[6,11],[11],
                                 [7],[7,12],[7,12,8],[8,12,13],[8,9,13],[13,9,14],[9,10,14],[10,14,15],[10,11,15],[11,15],[11],
                                 [12],[12,16],[12,16,13],[13,16,17],[13,14,17],[14,17,18],[14,15,18],[15,18],[15],
                                 [16],[16],[16,17],[17],[17,18],[18],[18]]
        connected_tiles = []

        # Combines the connected tile information (resource type, number) to each crossing
        for neighbouring_tiles in self.neighbouring_tiles:
            _tiles=[]
            for tile in neighbouring_tiles:
                _tiles.append(tiles[tile])
            connected_tiles.append(_tiles)

        # Crossing indexes where a harbour is located
        harbours_ind=[[0,1],[3,4],[6,15],[26,37],[45,53],[51,52],[47,48],[27,28],[7,17]]
        harbours_lst =[0]*len(self.neighbouring_crossings)

        # Sets the harbour type for each crossing
        for h,t in zip(harbours_ind,harbours):
            for ele in h:
                harbours_lst[ele] = t
        self.crossings = list(zip(self.neighbouring_crossings,connected_tiles,harbours_lst))
        self.building_state = [0]*len(connected_tiles)


    def place_settlement(self,crossing_index,player_num):
        self.building_state[crossing_index] = player_num


    def get_crossings(self):
        """
        Returns the crossing list containing all relevant information about the crossings.

        :return:
            list(tuple(neighbour_crossing_indices, neighbouring_tiles,harbours), length 54 (amount of crossings)
                Example of one list element: ([1, 8], [(1, 12)], 3) ... :
                Neighbouring Crossings indices: 1 and 8 , Neighbouring Tiles: Fields with number 12 (only 1 tile),
                Harbour: Ore 2:1
        """
        return self.crossings

    def get_neighbouring_crossings(self):
        """
        Returns neighbouring_crossings

        :return:
            list(list(int))
                Indices of the crossings adjacent to each crossing.
        """
        return self.neighbouring_crossings

    def get_neighbouring_tiles(self):
        """
        Returns neighbouring_tiles

        :return:
            list(list(int))
                Indices of the tiles adjacent to each crossing.
        """
        return self.neighbouring_tiles

    def get_building_state(self):
        """
        Returns relevant state information about the crossings, namely what building is placed at each crossing.

        :return:
            list(int) (length 54)
                Building type: 0 - no building, 1 - Settlement P1, 2 - Settlement P2, 3 - Settlement P3, 4 - Settlement P4
                5 - City P1, 6 - City P2, 7 - City P3, 8 - City P4
        """
        return self.building_state

    def get_possible_actions_build_settlement(self,player_num):
        """
        Returns all locations where settlement can be placed by the given player.

        :param player_num:
            Number of the player.

        :return valid_crossings:
            list(int) list of all crossing indexes where a settlement is allowed to be placed
                by this player
        """
        # Exception needed for initialization settlements
        ##############################################

        # Find all crossings a road of this player is connected to
        crossings_connected_to_roads = np.unique(self.get_roads()[self.get_state()==player_num])

        valid_crossings = np.zeros(Defines.NUM_CROSSINGS)

        # Iterate through all crossings a road of this player is connected to
        for crossing in crossings_connected_to_roads:
            valid_crossings[crossing] = 1 # assuming it is valid

            # Checks if there is a building on this crossing
            if self.building_state[crossing]>0:
                # If there is, the crossing is not valid for placing a settlement
                valid_crossings[crossing] = 0
                continue

            # Iterate through all crossings connected to this crossing
            for first_crossing in self.get_neighbouring_crossings()[crossing]:

                # Checks if there is a building on this crossing
                if self.building_state[first_crossing]>0:

                    # If there is, the crossing is not valid for placing a settlement
                    valid_crossings[crossing] = 0
                    break

        # Returns the remaining valid crossings
        return valid_crossings