from agent.traincatan import TrainCatan
from game.game import Game
import numpy as np
from agent.rl import DeepQNetwork

def update_state_action(player):
    state_space = env.get_state_space()
    possible_actions = env.get_possible_actions(player)
    return state_space,possible_actions

agent_number = [0]
random_player = [1]

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

done_cumilative  = [0, 0, 0, 0]
for episode in range(10000):
    reward_buffer = [0, 0, 0, 0]
    done_buffer = [0, 0, 0, 0]
    while True:
        if env.current_player - 1 in agent_number:

            if (not first_settlement):
                best_spot = env.get_best_spot_for_settlement_based_on_tile_numbers()
                env.build_settlement_at_crossing(best_spot)
                first_settlement = 1
                state_space,possible_actions = update_state_action(env.current_player)
            elif(not first_road):
                action = train.RL.choose_action(state_space, possible_actions)
                state_space, reward_buffer[env.current_player-1], possible_actions, done_buffer[env.current_player-1],clabel = env.step(action)
                first_road = 1

            elif (not second_settlement):
                best_spot = env.get_best_spot_for_settlement_based_on_tile_numbers()
                env.build_settlement_at_crossing(best_spot)
                second_settlement = 1
                state_space,possible_actions = update_state_action(env.current_player)

            elif(not second_road):
                action = train.RL.choose_action(state_space, possible_actions)
                state_space, reward_buffer[env.current_player-1], possible_actions, done_buffer[env.current_player-1],clabel = env.step(action)
                second_road = 1
            else:
                action = train.RL.choose_action(state_space, possible_actions)
                state_space, reward_buffer[env.current_player - 1], possible_actions, done_buffer[
                    env.current_player - 1], clabel = env.step(action)
        if env.current_player - 1 in random_player:
            action = np.random.choice(np.where(possible_actions == 1)[0])
            state_space, reward_buffer[env.current_player - 1], possible_actions, done_buffer[env.current_player - 1], clabel = env.step(action)
        else:
            buffer_player = env.current_player - 1
            action = train.RL.choose_action(state_space, possible_actions)
            state_space, reward_buffer[env.current_player-1], possible_actions, done_buffer[env.current_player-1],clabel = env.step(action)

        if(np.any(done_buffer) == 1):
            print("hi")
            print(done_buffer)
            done_cumilative = np.array(done_buffer) + np.array(done_cumilative)
            print(done_cumilative)
            break




