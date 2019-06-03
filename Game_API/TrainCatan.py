from Game import Game
from RL import DeepQNetwork
import numpy as np
from matplotlib import pyplot as plt
from xml import etree
import os
import pickle

class TrainCatan:

    def __init__(self,plot_interval=100,action_space='buildings_only',position_training_instances = (0,1,0,1),
                 needed_victory_points = 5,reward = 'building',
                 learning_rate=0.01,
                 reward_decay=0.99,
                 e_greedy=0,
                 replace_target_iter=200,
                 memory_size=100000,
                 num_games=5000,
                 final_epsilon=0.9,
                 epsilon_increase=0, #since which game the epsilon shall start to increase exponentially
                 softmax_choice= False,
                 opponents = 'random_sample'):
        self.plot_interval = plot_interval
        self.action_space = action_space

        self.position_training_instances = position_training_instances
        self.needed_victory_points,self.reward = needed_victory_points,reward
        self.learning_rate,self.reward_decay,self.e_greedy,self.replace_target_iter,self.memory_size = learning_rate,reward_decay,e_greedy,replace_target_iter,memory_size
        self.num_games = num_games
        self.final_epsilon = final_epsilon
        self.epsilon_increase = epsilon_increase
        self.softmax_choice = softmax_choice

        self.init_online_plot()
        self.init_training_environment()
        self.training_players = np.where(np.array(position_training_instances)==1)[0]
        self.state_space_buffer=[None,None,None,None]
        self.action_buffer=[None,None,None,None]
        self.reward_buffer=[None,None,None,None]


    def save_hyperparameters(self,filename):
        del(self.RL)
        if not os.path.exists('hyperparameters'):
            os.makedirs('hyperparameters')
        if not os.path.exists('hyperparameters/'+filename):
            os.makedirs('hyperparameters/'+filename)
        f = open('hyperparameters/'+filename+'/'+filename, 'wb')
        pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def load_hyperparameters(self,filename):
        if not os.path.exists('hyperparameters/'+filename):
            return
        f = open('hyperparameters/'+filename+'/'+filename, 'rb')
        return pickle.load(f)

    def init_taken_action_storage(self):
        self.donothing = [0,0,0,0]
        self.trade4vs1 = [0,0,0,0]
        self.buildroad = [0,0,0,0]
        self.buildsettlement = [0,0,0,0]
        self.buildcity = [0,0,0,0]
        self.trade3vs1 = [0,0,0,0]
        self.trade2vs1 = [0,0,0,0]

    def add_action_to_storage(self,clabel,player):
        if clabel == 'build_road':
            self.buildroad[player]+=1
        elif clabel == 'build_settlement':
            self.buildsettlement[player]+=1
        elif clabel == 'build_city':
            self.buildcity[player]+=1
        elif clabel == 'trade_4vs1':
            self.trade4vs1[player]+=1
        elif clabel == 'trade_3vs1':
            self.trade3vs1[player]+=1
        elif clabel == 'trade_2vs1':
            self.trade2vs1[player]+=1
        elif clabel == 'do_nothing':
            self.donothing[player]+=1

    def print_stored_actions(self):
        print('Do Nothing: '+str(self.donothing))
        print('Trade4vs1: '+str(self.trade4vs1))
        print('Trade3vs1: '+str(self.trade3vs1))
        print('Trade2vs1: '+str(self.trade2vs1))
        print('BuildRoad: '+str(self.buildroad))
        print('BuildSettlement: '+str(self.buildsettlement))
        print('BuildCity: '+str(self.buildcity))

    def start_training(self,training = True):
        self.init_taken_action_storage()
        eps_grad = -(self.num_games-self.epsilon_increase)/np.log(1-self.final_epsilon)
        step = 0
        for episode in range(self.num_games):
            # initial observation, get state space
            env = Game(random_init=False,action_space=self.action_space,needed_victory_points=self.needed_victory_points,reward=self.reward)

            state_space = env.get_state_space()
            possible_actions = env.get_possible_actions(env.current_player)

            iteration_counter = 0
            self.state_space_buffer=[None,None,None,None]
            self.action_buffer=[None,None,None,None]
            self.reward_buffer=[None,None,None,None]
            self.done_buffer=[None,None,None,None]
            
            done = 0
            while True:
                # fresh env
                # env.render()

                iteration_counter += 1
                # RL choose action based on state
                if env.current_player-1 in self.training_players:
                    buffer_player = env.current_player-1
                    self.action_buffer[buffer_player] = self.RL.choose_action(state_space,possible_actions)
                    state_space_, self.reward_buffer[buffer_player], possible_actions, self.done_buffer[buffer_player],clabel = env.step(self.action_buffer[buffer_player])
                    if env.current_player-1 != buffer_player: #When player one chooses do Nothing
                        self.state_space_buffer[buffer_player] = state_space
                    else:
                        #if train:
                        self.RL.store_transition(state_space, self.action_buffer[buffer_player], self.reward_buffer[buffer_player], state_space_)
                else:
                    action = np.random.choice(len(possible_actions), 1, p=possible_actions/sum(possible_actions))[0]
                    state_space_, r, possible_actions, d ,clabel= env.step(action)

                    if env.current_player-1 in self.training_players:
                        buffer_player = env.current_player-1
                        if self.state_space_buffer[buffer_player] is not None and self.action_buffer[buffer_player] is not None:# and train:
                            self.RL.store_transition(self.state_space_buffer[buffer_player], self.action_buffer[buffer_player], self.reward_buffer[buffer_player], state_space_)

                self.add_action_to_storage(clabel,env.current_player-1)

                # The game executes the action chosen by RL and gets next state and reward

                if (step > 2000) and (step % 50 == 0):# and training:
                    self.RL.learn()

                # swap observation
                state_space = state_space_

                # break while loop when end of this episode
                step += 1
                
                if np.all(np.array(self.done_buffer)[self.training_players]==1):
                    print(self.reward_buffer)
                    print('Game '+ str(episode)+' finished after ' + str(iteration_counter)+' iterations.####################################################')
                    print('Victory Points ' +str(env.get_victory_points())+'\n')
                    if training :
                        if episode > self.epsilon_increase:
                            self.RL.epsilon = 1-np.exp(-(episode-self.epsilon_increase)/eps_grad)
                    print('Epsilon '+str(self.RL.epsilon))
                    self.victories.append(np.argmax(env.get_victory_points()))
                    self.epsilons.append(self.RL.epsilon)
                    self.statistics.append(iteration_counter)

                    if (len(self.victories)%self.plot_interval==0) and (episode>0):
                        
                        self.plot_statistics_online(self.victories, self.epsilons,self.plot_interval)

                    break

                
        plt.show()
        # end of game
        print('Run Finished')
        self.print_stored_actions()

    def play_game(self,position_training_instances = (1,0,0,0),epsilon=1.0):
        if not hasattr(self,'RL'):
            print('No reinforcement learning instance available.')
            return
        self.RL.epsilon = epsilon
        self.training_players = np.where(np.array(position_training_instances)==1)[0]
        print(self.training_players)
        self.start_training(training=False)


    def init_training_environment(self):
        env = Game(action_space=self.action_space)
        self.RL = DeepQNetwork(len(env.get_possible_actions(1)), len(env.get_state_space()), # total action, total features/states
                      learning_rate=self.learning_rate,
                      reward_decay=self.reward_decay,
                      e_greedy=self.e_greedy,
                      replace_target_iter=self.replace_target_iter,
                      memory_size=self.memory_size,
                      softmax_choice=self.softmax_choice
                      )

    def init_online_plot(self):
        self.statistics = []
        self.victories = []
        self.epsilons = []
        plt.figure(2)
        plt.plot([],[],label='Player 1')
        plt.plot([],[],label='Player 2')
        plt.plot([],[],label='Player 3')
        plt.plot([],[],label='Player 4')
        plt.plot([],[],label='Epsilon')
        plt.legend()
        plt.xlabel('Game number')
        plt.ylabel('Winning percentage / Epsilon value')

    def plot_statistics_online(self,victories,epsilons,n_game_average):
        start_ind = 0
        end_ind = 0
        avg_vic = []
        avg_eps = []
        num_games = []
        while True:
            end_ind += n_game_average
            if end_ind > len(victories):
                end_ind = len(victories)
            num_games.append(end_ind-n_game_average/2)
            vic_extract = np.array(victories[start_ind:end_ind])
            eps_extract = epsilons[start_ind:end_ind]
            avg_vic.append([sum(np.where(vic_extract==0,1,0))/len(vic_extract),sum(np.where(vic_extract==1,1,0))/len(vic_extract)
                               ,sum(np.where(vic_extract==2,1,0))/len(vic_extract),sum(np.where(vic_extract==3,1,0))/len(vic_extract)])
            avg_eps.append(np.mean(eps_extract))
            if end_ind == len(victories):
                break
            start_ind = end_ind
        avg_vic = np.array(avg_vic)
        for i in range(4):
            plt.gca().lines[i].set_xdata(num_games)
            plt.gca().lines[i].set_ydata(avg_vic[:,i])
        plt.gca().lines[4].set_xdata(num_games)
        plt.gca().lines[4].set_ydata(avg_eps)
        plt.gca().relim()
        plt.gca().autoscale_view()
        plt.pause(0.05)

    def save_model(self):
        pass