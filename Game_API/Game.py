
# used to shuffle the deck of hexes
import random

import numpy as np
from scipy.sparse import coo_matrix
from Roads import Roads
from Crossings import Crossings
from HexTiles import HexTiles

class Game:

	def __init__(self,random_init=True):
		self.tiles = HexTiles(random_init)
		self.crossings = Crossings(self.tiles.get_tiles(),self.tiles.harbours)
		self.roads = Roads(self.crossings.get_neighbouring_crossings())
		self.building_state = self.crossings.get_building_state()
		self.dices_results = [2,3,3,4,4,4,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,9,9,9,9,10,10,10,11,11,12]

		self.cards = np.zeros((4,5))



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












