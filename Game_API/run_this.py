#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":
    d = DistributedTraining('randominitneuronnumbers',{'num_games' : [15000],'replace_target_iter':[100],'learning_rate':[0.3],
                                                       'layer1_neurons':[10,30,100,300,1000],'layer2_neurons':[10,30,100,300,1000]})

    

