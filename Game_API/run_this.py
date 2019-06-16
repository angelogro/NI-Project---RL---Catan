#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining
from TrainCatan import TrainCatan

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":
    """
    d = DistributedTraining('sigmoidborder',{'num_games' : [15000],'replace_target_iter':[100],'learning_rate':[0.3],
                                                       'layer1_neurons':[50],'layer2_neurons':[30],'verbose':[False],
                                                      'batch_size':[4096,4096,4096],'sigmoid_001_099_borders' : [(-1000,5000),
                                                                                                                 (-1000,7000),
                                                                                                                 (-1000,9000),
                                                                                                                 (1000,5000),
                                                                                                                 (1000,7000),
                                                                                                                 (1000,9000),
                                                                                                                 (3000,5000),
                                                                                                                 (3000,7000),
                                                                                                                 (3000,9000)]})
                                                                                                                 """
    t = TrainCatan()
    t.start_training()


    

