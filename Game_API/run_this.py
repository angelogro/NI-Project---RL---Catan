#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
# -----TO DO -------- Loop over for 4 players

train = None
if __name__ == "__main__":
    train = TrainCatan(plot_interval=100)
    train.start_training(5000,0.9)




