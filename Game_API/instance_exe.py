#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
import os
import sys
from DistributedTraining import DistributedTraining

# -----TO DO -------- Loop over for 4 players

if __name__ == "__main__":

    train = TrainCatan()

    setattr(train,sys.argv[1],int(sys.argv[2]))

    train.start_training()

