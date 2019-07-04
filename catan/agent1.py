from agent.traincatan import TrainCatan
from game.game import Game
import numpy as np
from agent.rl import DeepQNetwork

agent_number = [0]

train = TrainCatan(needed_victory_points=3, list_num_neurons=(50,), batch_size=32, output_graph=False,
                       learning_rate=0.5, softmax_choice=True,
                       memory_size=20000, sigmoid_001_099_borders=(-1000, 7000), replace_target_iter=200)

agentcatan = train.RL.load_model('2019-06-27.data-00000-of-00001')
# train.start_training(False)
env = Game(random_init=False,action_space="buildings_only",needed_victory_points=3,reward='victory_only')
# best_spot = env.get_best_spot_for_settlement_based_on_tile_numbers()
# env.build_settlement_at_crossing(best_spot)


state_space = env.get_state_space()
possible_actions = env.get_possible_actions(env.current_player)

first_settlement = 0
second_settlement = 0

while True:
    if env.current_player - 1 in agent_number:
        print("hi")
        if (not first_settlement):
            best_spot = env.get_best_spot_for_settlement_based_on_tile_numbers()
            env.build_settlement_at_crossing(best_spot)
            state_space = env.get_state_space()
            possible_actions = env.get_possible_actions(env.current_player)
            first_settlement = 1

    else:
        buffer_player = env.current_player - 1
        train.RL.choose_action(state_space, possible_actions)
