
# used to shuffle the deck of hexes
import random

import numpy as np
from scipy.sparse import coo_matrix

class Game:
	
	# different types of hexes
	HEX_FOREST = 5
	HEX_HILLS = 4
	HEX_MOUNTAINS = 3
	HEX_PASTURE = 2
	HEX_FIELDS = 1
	HEX_DESERT = 0
	PORT_ANY = 6

	NUM_CROSSINGS = 54



	def __init__(self,random_init=True):
		self.tiles = Hex_tiles(random_init)
		self.crossings = Crossings(self.tiles.get_tiles(),self.tiles.harbours)
		self.roads = Roads(self.crossings.get_neighbouring_crossings())
		self.building_state = self.crossings.get_building_state()
		self.dices_results = [2,3,3,4,4,4,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,9,9,9,9,10,10,10,11,11,12]

		self.cards = np.zeros((4,5))

		# Just for testing purposes
		self.place_settlement(8,1)
		self.place_settlement(30,1)
		self.place_settlement(40,1)
		self.place_road(12,1)
		self.place_road(13,1)
		self.place_road(14,1)

	# returns nextState,reward and whether the game is finished
	# General function which should be implemented at the end.
	def step(self,action):

		return None

	# OLD FUNCTION, CAN DEFINITELY BE REMOVED
	def get_possibleActions(self,player_num):
		#self.crossings_state = self.crossings.get_state()
		self.road_state = self.roads.get_state()

		# Initial placement
		actions =self.check_initialSettlement(player_num)

		actions+=self.check_place_road(player_num)
		return None

	# OLD FUNCTION, CAN DEFINITELY BE REMOVED
	def check_initialSettlement(self,player_num):
		# Returns actions array [DoNothing,placeInitSettlement,placeInitRoad]
		num_initsettlements = sum(self.crossings_state[self.crossings_state==player_num])

		if num_initsettlements<=2:
			if sum(self.road_state[self.road_state==player_num])<num_initsettlements:
				return [0,0,1]
			else:
				if num_initsettlements <2:
					return [0,1,0]
		return [1,0,0]

	def check_place_road(self,player_num):
		# Returns actions array [PlaceRoad@0,PlaceRoad@1,PlaceRoad@2 ....,PlaceRoad@71]
		pass

	def roll_dice(self):
		"""
		Rolls the dice.

		If it is a 7, the robber shall be moved. Otherwise distribute the corresponding resources.
		"""
		number = random.choice(self.dices_results)
		if number == 7:
			# Actually here we have to make sure that the next action taken by the player will be move_robber()
			self.move_robber()
		else:
			self.distribute_resources(number)

	def move_robber(self):
		pass

	def distribute_resources(self,number):
		"""
		Distribute the resources according to the rules.

		:param
			number:
				Number rolled by the dices.
		"""
		crossings = self.crossings.get_crossings()
		buildings = self.crossings.get_building_state()

		# Go through all crossings
		for i in range(len(crossings)):
			# Checks if there is no building on the crossing
			if buildings[i] == 0:
				continue
			# Iterate through all neighbouring tiles of the crossing
			for tile in crossings[i][1]:
				# If the rolled number is a number chip on one of those crossings
				if tile[1]==number:
					self.add_resource(tile[0]-1,(buildings[i]%4)-1)
					# If it is a town, add one more resource
					if buildings[i] > 4:
						self.add_resource(tile[0]-1,(buildings[i]%4)-1)


	def add_resource(self,resource_type,player_num):
		"""
		Adds a resource of resource_type to the stack of cards of player player_num.

		Checks if resource is available at all.
		:param
			resource_type:
				Resource_type to be added.
			player_num:
				Player the resource is added to.

		:return:
			bool
				True if the resource is available, False otherwise.
		"""
		if not self.check_resource_available_on_pile(resource_type):
			return
		self.cards[player_num,resource_type] += 1

	def check_resource_available_on_pile(self,resource_type):
		"""
		Checks if a certain resource type is still available to be drawn ba a player.

		:param resource_type:
			Resource_type to be checked.

		:return:
			bool
				True if the resource is available, False otherwise.
		"""
		if np.sum(self.cards[:,resource_type]) >= 19:
			return False
		return True

	# Placeholder
	def place_settlement(self,crossing_index,player_num):
		self.crossings.place_settlement(crossing_index,player_num)
		pass

	#Placeholder
	def place_road(self,road_index,player_num):
		self.roads.place_road(road_index,player_num)
		pass

	def get_possible_actions_build_settlement(self,player_num):
		"""
		Returns all locations where settlement can be placed by the given player.

		:param player_num:
			Number of the player.
		"""
		# Exception needed for initialization settlements
		 ##############################################

		# Find all crossings a road of this player is connected to
		crossings_connected_to_roads = np.unique(self.roads.get_roads()[self.roads.get_state()==player_num])

		valid_crossings = np.zeros(self.NUM_CROSSINGS)

		# Iterate through all crossings a road of this player is connected to
		for crossing in crossings_connected_to_roads:
			valid_crossings[crossing] = 1 # assuming it is valid

			# Checks if there is a building on this crossing
			if self.crossings.building_state[crossing]>0:
				# If there is, the crossing is not valid for placing a settlement
				valid_crossings[crossing] = 0
				continue

			# Iterate through all crossings connected to this crossing
			for first_crossing in self.crossings.get_neighbouring_crossings()[crossing]:

				# Checks if there is a building on this crossing
				if self.crossings.building_state[first_crossing]>0:

					# If there is, the crossing is not valid for placing a settlement
					valid_crossings[crossing] = 0
					break

		# Returns the remaining valid crossings
		return valid_crossings



class Hex_tiles:
	def __init__(self,random_init=True):
		"""
		Initializes the hexagonal game tiles together with the numbers on top of each tile.

		:param random_init:
			If true the tile locations, the numbers and the harbour order will be randomized.
			Else the basic game setup is used.
		"""
		self.harbours = [Game.HEX_MOUNTAINS,Game.HEX_PASTURE,Game.PORT_ANY,Game.PORT_ANY,
						 Game.HEX_FIELDS,Game.PORT_ANY,Game.HEX_HILLS,Game.PORT_ANY,
						 Game.HEX_FOREST]
		if random_init:
			# Resource Tiles
			available_numbers = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]

			tiles = [Game.HEX_FIELDS]*4+[Game.HEX_FOREST]*4+[Game.HEX_PASTURE]*4+\
				[Game.HEX_MOUNTAINS]*3+[Game.HEX_HILLS]*3

			random.shuffle(available_numbers)

			self.tiles = list(zip(tiles,available_numbers))+[(Game.HEX_DESERT,7)]
			random.shuffle(self.tiles)

			# Harbours
			random.shuffle(self.harbours)
		else:
			#Resource Tiles - fixed initial setup
			self.tiles = [(1, 4),(5,6),(1,9),(4,2),(5,5),(2,12),(2,4),(2,9),(4,8),(0,7),(3,8),\
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

class Roads:
	def __init__(self,neighbouring_crossings):
		"""
		Intializes the roads variables.

		"""
		roads = []
		for i in range(len(neighbouring_crossings)):
			for ele in neighbouring_crossings[i]:
				conn = [i,ele]
				conn.sort()
				roads.append(conn)
		roads = list(set(tuple(road) for road in roads))
		roads.sort()
		self.roads = roads
		self.road_state = [0]*len(roads)

	def get_roads(self):
		"""
		Return information about the road

		:return:
			list(tuple(tuple(int,int),int)) (length 72 - number of road positions)
				The first tuple describes the two crossings indices between which the road is situated.
				The integer describes the state of the road:
				Road type: 0 - no road, 1 - Road P1, 2 - Road P2, 3 - Road P3, 4 - Road P4

		"""
		return np.array(self.roads)

	def get_state(self):
		"""
		Returns relevant state information about the roads, namely what road is placed at each crossing.

		:return:
			list(int) (length 72)
				Road type: 0 - no road, 1 - Road P1, 2 - Road P2, 3 - Road P3, 4 - Road P4
		"""
		return np.array(self.road_state)

	def place_road(self,road_index,player_num):
		self.road_state[road_index] = player_num
