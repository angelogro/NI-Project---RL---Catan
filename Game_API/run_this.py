#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":
    d = DistributedTraining('learningratereplaceiter',{'num_games' : [300],'replace_target_iter':[20,40,60],'learning_rate':[5,1,0.5,0.1,0.05,0.01,0.005]})

    

