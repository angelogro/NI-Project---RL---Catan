"""
This part of code is the DQN brain, which is a brain of the agent.
All decisions are made in here.
Using Tensorflow to build the neural network.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/

Using:
Tensorflow: 1.0
gym: 0.7.3
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.special import softmax
import os

MODELFOLDER = '/models/'

np.random.seed(1)
tf.set_random_seed(1)


# Deep Q Network off-policy
class DeepQNetwork:
    def __init__(
            self,
            n_actions,  # Total actions
            n_features, # Total features/states
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.9,
            replace_target_iter=300,  # Num of iterations after which params of Q_Eval and Q_Target will be exchanged
            memory_size=500,
            batch_size=32,
            e_greedy_increment=None,
            output_graph=True,
            softmax_choice=False,
    ):
        # Initialize the params passed from run_this file
        self.summaries_dir = 'Summaries'
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = tf.Variable(learning_rate, trainable=False,dtype=tf.float64)
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.softmax_choice = softmax_choice
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max
        self.learn_step_counter = 0
        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

        # consist of [target_net, evaluate_net]
        self.sess = tf.InteractiveSession()
        self._build_net()
        # get_collection return the list of values associated with target_net_params & eval_net_params (refer to  _build_net)
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')


        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]



        if output_graph:
            # $ tensorboard --logdir=logs
            # tf.train.SummaryWriter soon be deprecated, use following
            tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        global_step_tensor = tf.Variable(0,trainable=False,name='global_step')
        self.sess.run(global_step_tensor.initializer)
        self.cost_his = []

    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')  # input
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss

        with tf.variable_scope('eval_net'):
            # c_names(collections_names) are the collections to store variables
            c_names, n_l1,n_l2, w_initializer, b_initializer = \
                ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 50,50, \
                tf.random_normal_initializer(0., 0.1), tf.constant_initializer(0.1)  # config of layers

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                self.w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                self.b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                self.l1 = tf.nn.tanh(tf.matmul(self.s, self.w1) + self.b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                self.w2 = tf.get_variable('w2', [n_l1, n_l2], initializer=w_initializer, collections=c_names)
                self.b2 = tf.get_variable('b2', [1, n_l2], initializer=b_initializer, collections=c_names)
                self.l2 = tf.nn.tanh(tf.matmul(self.l1, self.w2) + self.b2)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l3'):
                self.w3 = tf.get_variable('w3', [n_l2, self.n_actions], initializer=w_initializer, collections=c_names)
                self.b3 = tf.get_variable('b3', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.nn.tanh(tf.matmul(self.l1, self.w3) + self.b3)


        with tf.variable_scope('loss'):
            self.loss = tf.losses.huber_loss(self.q_target, self.q_eval)

        with tf.variable_scope('train') as self.train_var:
            self._train_op = tf.train.GradientDescentOptimizer(self.lr).minimize(self.loss)

        # ------------------ build target_net ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')    # input
        with tf.variable_scope('target_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                self.w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                self.b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                self.l1 = tf.nn.tanh(tf.matmul(self.s, self.w1) + self.b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                self.w2 = tf.get_variable('w2', [n_l1, n_l2], initializer=w_initializer, collections=c_names)
                self.b2 = tf.get_variable('b2', [1, n_l2], initializer=b_initializer, collections=c_names)
                self.l2 = tf.nn.tanh(tf.matmul(self.l1, self.w2) + self.b2)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l3'):
                self.w3 = tf.get_variable('w3', [n_l2, self.n_actions], initializer=w_initializer, collections=c_names)
                self.b3 = tf.get_variable('b3', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.nn.tanh(tf.matmul(self.l1, self.w3) + self.b3)

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size

        self.memory[index, :] = transition

        self.memory_counter += 1

    def choose_action(self, observation, possible_actions):
        # to have batch dimension when feed into tf placeholder
        observation = observation[np.newaxis, :]

        if np.random.uniform() < self.epsilon:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation}).flatten()

            possible_action_indices = np.where(possible_actions==1)[0]
            q_poss = actions_value[possible_action_indices]
            if self.learn_step_counter % self.replace_target_iter == 0:
                print('Possible action values: '+str(q_poss))
            if self.softmax_choice:

                q_softmax = softmax(q_poss)
                if self.learn_step_counter % self.replace_target_iter == 0:
                    print('Possible action values: '+str(q_poss))
                    print('Corresponding SOftmax values: '+str(q_softmax))
                return possible_action_indices[np.random.choice(len(q_softmax),1,p=q_softmax)[0]]

            action = possible_action_indices[np.argmax(q_poss)]
        else:
            action = np.random.choice(np.where(possible_actions==1)[0])
        return action

    def learn(self):
        #
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)

            #print('\ntarget_params_replaced\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)

        batch_memory = self.memory[sample_index, :]
#Train the eval net wrt to the batch memory
        q_next, q_eval = self.sess.run(
            [self.q_next, self.q_eval],
            feed_dict={
                self.s_: batch_memory[:, -self.n_features:],  # fixed params
                self.s: batch_memory[:, :self.n_features],  # newest params
            })

        # change q_target w.r.t q_eval's action
        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)


        # train eval network
        summary, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})

        self.cost_his.append(self.cost)

        # increasing epsilon
        #self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max

        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.figure(0)
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()

    def get_num_total_trainable_parameters(self):
        total_parameters = 0
        for variable in tf.trainable_variables():
            # shape is an array of tf.Dimension
            shape = variable.get_shape()
            variable_parameters = 1
            for dim in shape:
                variable_parameters *= dim.value

            total_parameters += variable_parameters
        return total_parameters


    def variable_summaries(self,var):
        """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
        with tf.name_scope('summaries'):
            mean = tf.reduce_mean(var)
            tf.summary.scalar('mean', mean)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
            tf.summary.scalar('stddev', stddev)
            tf.summary.scalar('max', tf.reduce_max(var))
            tf.summary.scalar('min', tf.reduce_min(var))
            tf.summary.histogram('histogram', var)

    def save_current_model(self,model_name):
        self.saver = tf.train.Saver()
        self.saver.save(self.sess,os.getcwd()+MODELFOLDER +model_name)

    def save_model_interval(self,model_name,global_step=1000):
        self.saver = tf.train.Saver()
        self.saver.save(self.sess,os.getcwd()+MODELFOLDER +model_name,global_step=global_step)

    def load_model(self,model_name):
        self.saver = tf.train.import_meta_graph(os.getcwd()+MODELFOLDER+model_name)
        self.saver.restore(self.sess,tf.train.latest_checkpoint(os.getcwd()+MODELFOLDER+'./'))



