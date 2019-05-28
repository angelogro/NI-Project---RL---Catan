from Game import Game
from RL import DeepQNetwork
import numpy as np
from matplotlib import pyplot as plt

class TrainCatan:

    def __init__(self,plot_interval=100,action_space='buildings_only',position_training_instances = (1,1,0,0),opponents = 'random_sample'):
        self.plot_interval = plot_interval
        self.action_space = action_space
        self.init_online_plot()
        self.init_training_environment()
        self.training_players = np.where(np.array(position_training_instances)==1)[0]
        self.state_space_buffer=[None,None,None,None]
        self.action_buffer=[None,None,None,None]




    def start_training(self,num_games,final_epsilon=0.99):
        eps_grad = -num_games/np.log(1-final_epsilon)
        step = 0
        for episode in range(num_games):
            # initial observation, get state space
            env = Game(random_init=False,action_space=self.action_space,needed_victory_points=3,reward='victory_only')

            state_space = env.get_state_space()
            possible_actions = env.get_possible_actions(env.current_player)

            iteration_counter = 0
            state_space_p1 = None
            action_p1 = None
            reward = None
            done = 0
            while True:
                # fresh env
                # env.render()

                iteration_counter += 1
                # RL choose action based on state

                if env.current_player-1 in self.training_players:
                    buffer_player = env.current_player-1
                    self.action_buffer[buffer_player] = self.RL.choose_action(state_space,possible_actions)
                    state_space_, reward, possible_actions, done = env.step(self.action_buffer[buffer_player])
                    if env.current_player-1 != buffer_player: #When player one chooses do Nothing
                        self.state_space_buffer[buffer_player] = state_space
                    else:
                        self.RL.store_transition(state_space, self.action_buffer[buffer_player], reward, state_space_)
                else:
                    action = np.random.choice(len(possible_actions), 1, p=possible_actions/sum(possible_actions))[0]
                    state_space_, r, possible_actions, d = env.step(action)
                    if env.current_player-1 in self.training_players:
                        buffer_player = env.current_player-1
                        if self.state_space_buffer[buffer_player] is not None and self.action_buffer[buffer_player] is not None:
                            self.RL.store_transition(self.state_space_buffer[buffer_player], self.action_buffer[buffer_player], reward, state_space_)


                # The game executes the action chosen by RL and gets next state and reward

                if (step > 2000) and (step % 10 == 0) :
                    self.RL.learn()


                # swap observation
                state_space = state_space_

                # break while loop when end of this episode
                if done:
                    print('Game '+ str(episode)+' finished after ' + str(iteration_counter)+' iterations.####################################################')
                    print('Victory Points ' +str(env.get_victory_points())+'\n')
                    self.RL.epsilon = 1-np.exp(-episode/eps_grad)
                    print('Epsilon '+str(self.RL.epsilon))
                    self.victories.append(np.argmax(env.get_victory_points()))
                    self.epsilons.append(self.RL.epsilon)
                    self.statistics.append(iteration_counter)

                    if episode%self.plot_interval==0 and episode>0:
                        self.plot_statistics_online(self.victories, self.epsilons,self.plot_interval)

                    break

                step += 1
        plt.show()
        # end of game
        print('Run Finished')


    def init_training_environment(self):
        env = Game(action_space=self.action_space)
        self.RL = DeepQNetwork(len(env.get_possible_actions(1)), len(env.get_state_space()), # total action, total features/states
                      learning_rate=0.01,
                      reward_decay=0.99,
                      e_greedy=0,
                      # e_greedy_increment=0.00005,
                      replace_target_iter=200,
                      memory_size=100000
                      # output_graph=True
                      )

    def init_online_plot(self):
        self.statistics = []
        self.victories = []
        self.epsilons = []
        self.num_games = []
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