#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining
from TrainCatan import TrainCatan

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":

    d = DistributedTraining('rewarddecay',{'reward_decay':[1,0.98,0.96,0.94,0.92,0.9,0.88,0.86],'num_games' : [15000],'random_init': [True],'reward':['building'],
                                                 'random_shuffle_training_players_':[True],'needed_victory_points':[4,5],
                                             'replace_target_iter':[100],'learning_rate':[0.3],
                                                       'layer1_neurons':[50],'layer2_neurons':[30],'verbose':[False],
                                                      'sigmoid_001_099_borders' : [(-1000,11000)],
                                             'learning_rate_decay_factor':[0.9998],'batch_size':[4096,4096],
                                                'learning_rate_start_decay':[8000]
                                             })
    """
    train = TrainCatan(needed_victory_points=6)
    train.RL.load_model('randominitreward13.data-00000-of-00001')
    train.RL.epsilon = 1
    train.start_training(training=False)
    """





    

