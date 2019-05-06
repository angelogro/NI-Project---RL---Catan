
import Defines
import random
import numpy as np
from scipy.sparse import coo_matrix

class HexTiles:
    def __init__(self,random_init=True):
        """
        Initializes the hexagonal game tiles together with the numbers on top of each tile.

        :param random_init:
            If true the tile locations, the numbers and the harbour order will be randomized.
            Else the basic game setup is used.
        """
        self.harbours = [Defines.HEX_MOUNTAINS,Defines.HEX_PASTURE,Defines.PORT_ANY,Defines.PORT_ANY,
                         Defines.HEX_FIELDS,Defines.PORT_ANY,Defines.HEX_HILLS,Defines.PORT_ANY,
                         Defines.HEX_FOREST]
        if random_init:
            # Resource Tiles
            available_numbers = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]

            tiles = [Defines.HEX_FIELDS]*4+[Defines.HEX_FOREST]*4+[Defines.HEX_PASTURE]*4+ \
                    [Defines.HEX_MOUNTAINS]*3+[Defines.HEX_HILLS]*3

            random.shuffle(available_numbers)

            self.tiles = list(zip(tiles,available_numbers))+[(Defines.HEX_DESERT,7)]
            random.shuffle(self.tiles)

            # Harbours
            random.shuffle(self.harbours)
        else:
            #Resource Tiles - fixed initial setup
            self.tiles = [(1, 4),(5,6),(1,9),(4,2),(5,5),(2,12),(2,4),(2,9),(4,8),(0,7),(3,8), \
                          (2,10),(5,3),(3,5),(4,10),(5,11),(1,3),(1,6),(3,11)]


    def get_tiles(self):
        """
        Returns the tiles variable.

        :return:
            list(tuple(int,int)): Tiles list with the index of the element describing the position of the tile.
            The two integers describe the resource type and the number on top of the tile respectively.
            Tile positions according to index:
                00 01 02
              03 04 05 06
             07 08 09 10 11
              12 13 14 15
               16 17 18
        """
        return self.tiles

    def print_tiles(self):
        """
        Prints the tiles inside the board layout with a combination of a letter and a 2 digit number representing
        each tile.

        The letters are D - Desert, G - Grain, P - Pasture, M - Mountain, F - Forrest and the numbers represent
        the number on top of the tile (ranging from 2 - 12)
        """
        ind=0
        numTilesperRow=[3,4,5,4,3]
        #				Desert   Grain  Pasture  Mountain  Hills Forrest
        tile_dict = {'0' : 'D','1':'G','2':'P','3':'M','4':'H','5':'F'}
        for row in numTilesperRow:
            tiles_part = self.tiles[ind:ind+row]
            print(''.join([' ']*(5-row)*2),end='')
            for ele in tiles_part:
                print(tile_dict.get(str(ele[0])),end = '')
                print("{:02d}".format(ele[1]),end = ' ')
            print('')
            ind=ind+row



    # returns one hot representation of tiles and numbers
    def get_tile_state(self):
        """
        Returns the tiles state of the board in a 1-D-Array form.

        :return:
            np.array() (length 123)
            Tile Nr. 0    1    2  ...
            Indices 0:5,6:11,12:17 ...
            The entry for each subrange of indices represents the number on top of the tile.
            The entry location within the subrange of indices represents the type of resource.
            Example:[0,0,0,0,6,0,0,0,9,0,0,0 ...] means: Tile 0: Number 6, Resource Type Wood, Tile 1: Number 9, Resource Tyoe Mountains
            19x6 = 114 entries correspond to terrain tiles, the last 9 entries correspond to harbour
            types starting from the top left and going clockwise around the island.
        """
        rows  = range(19)
        cols = list(list(zip(*self.tiles))[0])
        data = list(list(zip(*self.tiles))[1])
        tiles_vector = np.ravel(coo_matrix((data, (rows, cols)), shape=(19,6)).toarray())
        return tiles_vector

    def get_harbour_state(self):
        return np.array(self.harbours)