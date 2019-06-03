#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
# -----TO DO -------- Loop over for 4 players

train = None
if __name__ == "__main__":
    train = TrainCatan(num_games=5000,final_epsilon=0.9,needed_victory_points=3,reward='victory_only',
                       action_space='buildings_only',position_training_instances=(1,0,0,0),epsilon_increase=1000,
                       softmax_choice=True,learning_rate=0.005,memory_size=50000)
    train.start_training()
    print(train.RL.b1.eval())
    print(train.RL.w2.eval())
    train.num_games = 200
    train.play_game(epsilon=0.9)
    print(train.RL.b1.eval())
    print(train.RL.w2.eval())





