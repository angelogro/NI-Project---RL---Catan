#!/usr/bin/env python
# coding: utf-8

# In[9]:


from Game import Game
from RL import DeepQNetwork
import numpy as np
from matplotlib import pyplot as plt
# -----TO DO -------- Loop over for 4 players

statistics = []
victories = []
epsilons = []
def run_Game():
    step = 0

    for episode in range(3000):
        # initial observation, get state space
        env = Game(random_init=False,action_space='buildings_only',needed_victory_points=3,reward='victory_only')
        # -----TO DO -------- Should have a method in Game to return the state space getStateSpace()
        state_space = env.get_state_space()
        possible_actions = env.get_possible_actions(env.current_player)
        print(env.act_dic)
        #print('Initial State Space',state_space)
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
            if env.current_player == 1:
                action_p1 = RL.choose_action(state_space,possible_actions)
                state_space_, reward, possible_actions, done = env.step(action_p1)
                if env.current_player != 1: #When player one chooses do Nothing
                    state_space_p1 = state_space
                else:
                    RL.store_transition(state_space, action_p1, reward, state_space_)
            else:
                action = np.random.choice(len(possible_actions), 1, p=possible_actions/sum(possible_actions))[0]
                state_space_, r, possible_actions, d = env.step(action)
                if env.current_player==1:
                    RL.store_transition(state_space_p1, action_p1, reward, state_space_)


            # The game executes the action chosen by RL and gets next state and reward

            if (step > 2000) and (step % 10 == 0) :
                #if RL.epsilon > 0.4:
                #    RL.trigger_adapt_learning_rate()
                RL.learn()


            # swap observation
            state_space = state_space_

            # break while loop when end of this episode
            if done:
                print('Game '+ str(episode)+' finished after ' + str(iteration_counter)+' iterations.####################################################')
                print('Victory Points ' +str(env.get_victory_points())+'\n')
                print('Epsilon '+str(RL.epsilon))
                victories.append(np.argmax(env.get_victory_points()))
                epsilons.append(RL.epsilon)
                statistics.append(iteration_counter)


                break

            step += 1

    # end of game
    print('game over')
    plot_statistics(victories, epsilons,100)
    #env.destroy()

def plot_statistics(victories,epsilons,n_game_average):
    # create moving average
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
    plt.figure(1)
    plt.plot(num_games,avg_vic[:,0],label='Player 1')
    plt.plot(num_games,avg_vic[:,1],label='Player 2')
    plt.plot(num_games,avg_vic[:,2],label='Player 3')
    plt.plot(num_games,avg_vic[:,3],label='Player 4')
    plt.plot(num_games,avg_eps,label='Epsilon')
    plt.xlabel('Game number')
    plt.ylabel('Winning percentage / Epsilon value')
    plt.legend()

RL = None
if __name__ == "__main__":
    # Initilize the DQN and run the game
    env = Game(action_space='buildings_only')
    print(len(env.get_possible_actions(1)))
    RL = DeepQNetwork(len(env.get_possible_actions(1)), len(env.get_state_space()), # total action, total features/states
                      learning_rate=0.01,
                      reward_decay=0.99,
                      e_greedy=0.9,
                      e_greedy_increment=0.00005,
                      replace_target_iter=200,
                      memory_size=100000
                      # output_graph=True
                      )
    #sleep(100)
    run_Game()
    #env.mainloop()

    RL.plot_cost()


# In[ ]:




