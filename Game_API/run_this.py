#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
import os

# -----TO DO -------- Loop over for 4 players

train = None
if __name__ == "__main__":
    print(os.getcwd())
    
    train = TrainCatan(num_games=10000,final_epsilon=0.9,needed_victory_points=3,reward='victory_only',
                       action_space='buildings_only',position_training_instances=(1,0,0,0),epsilon_increase=1000,
                       softmax_choice=False,learning_rate=2,memory_size=50000,sigmoid_001_009_borders=(1000,5000),
                       reward_decay=0.9,plot_interval=100,autosave=True,random_shuffle_training_players=True,
                       random_init=False)
                 
    #train.RL.save_current_model(str(datetime.date.today()))
    train.start_training()
    #print(train.RL.b1.eval())
    #print(train.RL.w2.eval())
    #train.num_games = 500
    #train.play_game(epsilon=1)
    #print(train.RL.b1.eval())
    #print(train.RL.w2.eval
    

