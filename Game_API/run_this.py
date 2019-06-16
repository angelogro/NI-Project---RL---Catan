#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining
from TrainCatan import TrainCatan

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":
    d = DistributedTraining('randominitshuffle',{'num_games' : [15000],'random_init': [True,False],'reward':['building','victory_only'],
                                                 'random_shuffle_training_players_':[True,False],
                                             'replace_target_iter':[100],'learning_rate':[0.3],
                                                       'layer1_neurons':[50],'layer2_neurons':[30],'verbose':[False],
                                                      'sigmoid_001_099_borders' : [(-1000,7000)],
                                             'learning_rate_decay_factor':[0.9995],'batch_size':[4096,4096,4096,4096],
                                             })



    

