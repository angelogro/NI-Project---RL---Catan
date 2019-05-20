#!/usr/bin/env python
# coding: utf-8

# In[9]:


from Game import Game
from RL import DeepQNetwork
# -----TO DO -------- Loop over for 4 players

statistics = []
def run_Game():
    step = 0

    for episode in range(5000):
        # initial observation, get state space
        env = Game(random_init=False,action_space='buildings_only',needed_victory_points=3,reward='building')
        # -----TO DO -------- Should have a method in Game to return the state space getStateSpace()
        state_space = env.get_state_space()
        possible_actions = env.get_possible_actions(env.current_player)
        print(env.act_dic)
        #print('Initial State Space',state_space)
        iteration_counter = 0
        while True:
            # fresh env
           # env.render()
            iteration_counter += 1
            # RL choose action based on state
            action = RL.choose_action(state_space,possible_actions)

            # The game executes the action chosen by RL and gets next state and reward
            
            state_space_, reward, possible_actions, done = env.step(action)

           # -----TO DO -------- How to store the memory wrt to the player
            
            RL.store_transition(state_space, action, reward, state_space_)

            if (step > 200) and (step % 20 == 0):
                RL.learn()

            # swap observation
            state_space = state_space_

            # break while loop when end of this episode
            if done:
                print('Game '+ str(episode)+' finished after ' + str(iteration_counter)+' iterations.####################################################')
                print('Victory Points ' +str(env.get_victory_points())+'\n')
                print(RL.epsilon)
                statistics.append(iteration_counter)
                break

            step += 1

    # end of game
    print('game over')
    #env.destroy()


if __name__ == "__main__":
    # Initilize the DQN and run the game
    env = Game(action_space='buildings_only')
    print(len(env.get_possible_actions(1)))
    RL = DeepQNetwork(len(env.get_possible_actions(1)), len(env.get_state_space()), # total action, total features/states
                      learning_rate=0.005,
                      reward_decay=0.97,
                      e_greedy=0.9,
                      e_greedy_increment=0.0001,
                      replace_target_iter=200,
                      memory_size=2000
                      # output_graph=True
                      )
    #sleep(100)
    run_Game()
    #env.mainloop()

    RL.plot_cost()


# In[ ]:




