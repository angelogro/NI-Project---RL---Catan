#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":
    d = DistributedTraining('learningrates',{'learning_rate':[5,1,0.5,0.1,0.05,0.01,0.005]})

    

