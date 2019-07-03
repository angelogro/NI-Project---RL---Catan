from agent.traincatan import TrainCatan
from game.game import Game
from agent.rl import DeepQNetwork


train = TrainCatan(needed_victory_points=3, list_num_neurons=(50,), batch_size=32, output_graph=False,
                       learning_rate=0.5, softmax_choice=True,
                       memory_size=20000, sigmoid_001_099_borders=(-1000, 7000), replace_target_iter=200)
agentcatan = train.RL.load_model('2019-07-01.data-00000-of-00001')

env = Game(random_init=False,action_space="buildings_only",needed_victory_points=3,reward='victory_only')

env.get_settlement_placement_scores()