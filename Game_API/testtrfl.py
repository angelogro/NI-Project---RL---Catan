from T_QNetwork import QNetwork
from Game import Game
import tensorflow as tf
import numpy as np

from collections import deque
class Memory():
    def __init__(self, max_size = 1000):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)),
                               size=batch_size,
                               replace=False)
        return [self.buffer[ii] for ii in idx]


train_episodes = 700          # max number of episodes to learn from
max_steps = 200                # max steps in an episode
gamma = 0.99                   # future reward discount

# Exploration parameters
explore_start = 1.0            # exploration probability at start
explore_stop = 0.01            # minimum exploration probability
decay_rate = 0.0001            # exponential decay rate for exploration prob

# Network parameters
hidden_size = 64               # number of units in each Q-network hidden layer
learning_rate = 0.001         # Q-network learning rate

# Memory parameters
memory_size = 100000            # memory capacity
batch_size = 20                # experience mini-batch size
pretrain_length = batch_size   # number experiences to pretrain the memory


# Initialize the game
env = Game(random_init=False,action_space='buildings_only',needed_victory_points=3,reward='victory_only')

tf.reset_default_graph()
mainQN = QNetwork(name='main', hidden_size=hidden_size, learning_rate=learning_rate,state_size=len(env.get_state_space()), action_size=len(env.get_possible_actions(1)),batch_size=batch_size)

# Take one random step to get the game started
action = np.random.choice(np.where(env.get_possible_actions(env.current_player)==1)[0])
state, reward, action , done, _ = env.step(action)

memory = Memory(max_size=len(env.get_possible_actions(1)))

# Make a bunch of random actions and store the experiences
for ii in range(pretrain_length):
    # Make a random action
    #action = env.get_possible_actions(env.current_player).sample()
    action = np.random.choice(np.where(env.get_possible_actions(env.current_player)==1)[0])
    next_state, reward, action, done, _ = env.step(action)

    if done:
        # The simulation fails so no next state
        next_state = np.zeros(state.shape)
        # Add experience to memory
        memory.add((state, action, reward, next_state))

        # Start new episode
        env.reset()
        # Take one random step to get the get the game started
        action = np.random.choice(np.where(env.get_possible_actions(env.current_player)==1)[0])
        state, reward, action , done, _ = env.step(action)
    else:
        # Add experience to memory
        memory.add((state, action, reward, next_state))
        state = next_state


