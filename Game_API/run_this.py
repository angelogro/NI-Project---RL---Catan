#!/usr/bin/env python
# coding: utf-8

from DistributedTraining import DistributedTraining
from TrainCatan import TrainCatan

# -----TO DO -------- Loop over for 4 players

train = None
d = None
if __name__ == "__main__":

    d = DistributedTraining('init',{'learning_rate':[0.01],'reward_decay':[0.95],
                                            'list_num_neurons':[(50,),(100,),(30,),(1000,)],
                                                 'random_shuffle_training_players_':[False],'needed_victory_points':[3],
                                             'replace_target_iter':[500],'verbose':[False],'memory_size':[20000],
                                                      'sigmoid_001_099_borders' : [(0,15000)],'show_cards_statistic':[True],
                                             'batch_size':[1024],
                                                'learning_rate_start_decay':[10000],
        'num_games' : [30000,30000],'random_init': [True],'reward':['cards'],'learning_rate_decay_factor':[0.9998]
                                             })
    """
    train = TrainCatan(needed_victory_points=3,list_num_neurons=(50,),batch_size=1024,output_graph=False,learning_rate=0.01,reward='cards',
			memory_size = 20000,sigmoid_001_099_borders=(0,15000),replace_target_iter=500,reward_decay=0.95,num_games=30000,learning_rate_decay_factor=0.9998,
                       learning_rate_start_decay=10000,show_cards_statistic=True,random_init=True)
    #train.RL.load_model('learningrate13.data-00000-of-00001')
    #train.RL.epsilon = 1
    train.start_training()
    """









    

