#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
from PlayCatan import PlayCatan
# -----TO DO -------- Loop over for 4 players

train = None
if __name__ == "__main__":
     #train = TrainCatan(plot_interval=100,action_space='building_and_trade',position_training_instances=(1,0,0,0))
     #train.start_training()
     play = PlayCatan()
     play.start_playing()



