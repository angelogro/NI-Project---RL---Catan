#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
# -----TO DO -------- Loop over for 4 players

train = None
if __name__ == "__main__":
    train = TrainCatan(num_games=100,final_epsilon=0.99,needed_victory_points=3,reward='victory_only',action_space='buildings_only',position_training_instances=(1,0,0,0))
    train.start_training()
    print(train.RL.b1.eval())
    print(train.RL.w2.eval())
    train.num_games = 100
    train.play_game((1,0,0,0))
    print(train.RL.b1.eval())
    print(train.RL.w2.eval())





