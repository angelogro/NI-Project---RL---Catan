
# used to shuffle the deck of hexes
import random

import numpy as np
from scipy.sparse import coo_matrix
from Roads import Roads
from Crossings import Crossings
from HexTiles import HexTiles
import Defines

class Game:

	def __init__(self,random_init=True):
		self.tiles = HexTiles(random_init)
		self.crossings = Crossings(self.tiles.get_tiles(),self.tiles.harbours)
		self.roads = Roads(self.crossings.get_neighbouring_crossings())
		self.crossings.create_connected_roads(self.roads.get_roads())
		self.building_state = self.crossings.get_building_state()
		self.dices_results = [2,3,3,4,4,4,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,9,9,9,9,10,10,10,11,11,12]


		# 4 players, 5 resources
		self.cards = np.zeros((4,5))

		self.current_player = 1

	def next_players_turn(self):
		self.current_player =  self.current_player + 1 if self.current_player < 4 else 1

	# returns nextState,reward and whether the game is finished
	# General function which should be implemented at the end.
	def step(self,action):

		# Make state transition
		self.perform_action(action)
		# If action is 'Do Nothing'
		self.next_players_turn()
		pass

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
		self.pay(player_num,buying_good='Settlement')
		self.crossings.place_settlement(crossing_index,player_num)
		pass

	#Placeholder
	def place_road(self,road_index,player_num):
		self.pay(player_num,buying_good='Road')
		self.roads.place_road(road_index,player_num)
		pass

	def place_city(self,crossing_index,player_num):
		self.pay(player_num,buying_good='City')
		self.crossings.place_city(crossing_index,player_num)
		pass

	def get_possible_actions_build_settlement(self,player_num,init_state=False):
		"""
        Returns all locations where settlement can be placed by the given player.

        :param player_num:
            Number of the player.

        :return valid_crossings:
            list(int) list of all crossing indexes where a settlement is allowed to be placed
                by this player
        """
		valid_crossings = np.zeros(Defines.NUM_CROSSINGS)

		# On Initialization
		if init_state:
			return self.crossings.get_building_state()==0

		# Find all crossings a road of this player is connected to
		crossings_connected_to_roads = np.unique(self.roads.get_roads()[self.roads.get_state()==player_num])

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
				if self.crossings.building_state[first_crossing]>0 and self.crossings.building_state[first_crossing]<9:

					# If there is, the crossing is not valid for placing a settlement
					valid_crossings[crossing] = 0
					break

		# Returns the remaining valid crossings
		return valid_crossings

	def get_possible_actions_build_road(self,player_num,init_state = False):
		"""
		Returns a vector of zeros of length of amount of roads.
		with ones on indices where roads can be placed by the given player.

		:param player_num:
			Number of the player.
		"""
		# On initialization
		if init_state == True:
			# Find the settlement without a road close to it
			# Find indices of crossings with buildings
			ind_with_buildings = np.ravel(np.argwhere(self.crossings.get_building_state()==player_num))

			# Loop through all settlement of this player
			for crossing_index in ind_with_buildings:
				connected_roads = self.roads.get_state()

				# If no road connected to the settlement yet...
				if np.sum(connected_roads[self.crossings.connected_roads[crossing_index]])==0:
					final_arr = np.zeros(Defines.NUM_EDGES)
					final_arr[self.crossings.connected_roads[crossing_index]]=1
					return final_arr
			return

		# During normal gameplay...

		# Find all roads of player player_num and look for edges they are connected to
		conn_roads = np.array(self.roads.connected_roads)
		road_state = np.array(self.roads.road_state)
		list_conn = conn_roads[np.where(road_state==player_num)]

		# Convert those connected edges to an array of zeros with a one where a road can be placed
		final_list = []
		for lst in list_conn:
			final_list.extend(lst)
		final_arr = np.zeros(Defines.NUM_EDGES)
		final_arr[final_list]=1

		# Exclude all occupied edges from the list of connected edges and return result
		return np.logical_and(np.logical_not(road_state),final_arr)

	def check_resources_available(self,player_num,buying_good):
		"""
        Check availability of resources for the specific buying good.

        :param player_num:
            Number of the player.

				buying_good:
			One of the following: 'Road', 'Settlement', 'City', 'Development Card'
        """
		if buying_good=='Road':
			return (self.cards[player_num-1,:]>=np.array([0,0,0,1,1])).all()
		if buying_good=='Settlement':
			return (self.cards[player_num-1,:]>=np.array([1,1,0,1,1])).all()
		if buying_good=='City':
			return (self.cards[player_num-1,:]>=np.array([2,0,3,0,0])).all()
		if buying_good=='Development Card':
			return (self.cards[player_num-1,:]>=np.array([1,1,1,0,0])).all()

	def pay(self,player_num,buying_good):
		"""
        Reduces the cards of others player by the amount needed for the resources.

        :param player_num:
            Number of the player.

				buying_good:
			One of the following: 'Road', 'Settlement', 'City', 'Development Card'
        """
		if buying_good=='Road':
			self.cards[player_num-1,:]-np.array([0,0,0,1,1])
		if buying_good=='Settlement':
			self.cards[player_num-1,:]-np.array([1,1,0,1,1])
		if buying_good=='City':
			self.cards[player_num-1,:]-np.array([2,0,3,0,0])
		if buying_good=='Development Card':
			self.cards[player_num-1,:]-np.array([1,1,1,0,0])

	def get_possible_actions_build_city(self,player_num):
		"""
        Returns all locations where cities can be placed by the given player.

        :param player_num:
            Number of the player.

        :return valid_crossings:
            list(int) list of all crossing indexes where a city is allowed to be placed
                by this player
        """
		valid_crossings = self.crossings.get_building_state()==player_num
		# Returns the remaining valid crossings
		return valid_crossings








