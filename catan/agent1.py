from agent.traincatan import TrainCatan
from game.game import Game
import numpy as np
from agent.rl import DeepQNetwork

def update_state_action(player):
    state_space = env.get_state_space()
    possible_actions = env.get_possible_actions(player)
    return state_space,possible_actions

agent_number = [0]

train = TrainCatan(needed_victory_points=3, list_num_neurons=(50,), batch_size=32, output_graph=False,
                       learning_rate=0.5, softmax_choice=True,
                       memory_size=20000, sigmoid_001_099_borders=(-1000, 7000), replace_target_iter=200)

agentcatan = train.RL.load_model('2019-06-27.data-00000-of-00001')

env = Game(random_init=False,action_space="buildings_only",needed_victory_points=3,reward='victory_only')

state_space = env.get_state_space()
possible_actions = env.get_possible_actions(env.current_player)

first_settlement = 0
second_settlement = 0
first_road = 0
second_road = 0

while True:
    if env.current_player - 1 in agent_number:

        if (not first_settlement):
            best_spot = env.get_best_spot_for_settlement_based_on_tile_numbers()
            env.build_settlement_at_crossing(best_spot)
            state_space = env.get_state_space()
            possible_actions = env.get_possible_actions(env.current_player)
            first_settlement = 1
            state_space,possible_actions = update_state_action(env.current_player)
        elif(not first_road):
            action = train.RL.choose_action(state_space, possible_actions)
            env.step(action)
            first_road = 1
            possible_actions = env.get_possible_actions(env.current_player)

        elif (not second_settlement):
            best_spot = env.get_best_spot_for_settlement_based_on_tile_numbers()
            env.build_settlement_at_crossing(best_spot)
            state_space = env.get_state_space()
            possible_actions = env.get_possible_actions(env.current_player)
            second_settlement = 1
            possible_actions = env.get_possible_actions(env.current_player)

        elif(not second_road):
            action = train.RL.choose_action(state_space, possible_actions)
            env.step(action)
            second_road = 1
            possible_actions = env.get_possible_actions(env.current_player)

    else:
        buffer_player = env.current_player - 1
        action = train.RL.choose_action(state_space, possible_actions)
        env.step(action)
        possible_actions = env.get_possible_actions(env.current_player)


