#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining
from TrainCatan import TrainCatan

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":

    d = DistributedTraining('learningrate',{'num_games' : [15000],'random_init': [False],'reward':['victory'],'learning_rate_decay_factor':[0.9998],
                                            'learning_rate':[3,1,0.3,0.1,0.03,0.01,0.003,0.001],'reward_decay':[1,0.95],
                                                 'random_shuffle_training_players_':[False],'needed_victory_points':[3],
                                             'replace_target_iter':[100],'verbose':[False],
                                                      'sigmoid_001_099_borders' : [(-1000,7000)],
                                             'batch_size':[4096,4096],
                                                'learning_rate_start_decay':[5000]
                                             })
    """
    train = TrainCatan(needed_victory_points=6)
    train.RL.load_model('randominitreward13.data-00000-of-00001')
    train.RL.epsilon = 1
    train.start_training(training=False)
    """





    

