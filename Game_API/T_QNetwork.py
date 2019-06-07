import trfl
import tensorflow as tf

class QNetwork:
    def __init__(self, learning_rate=0.01, state_size=4,
                 action_size=2, hidden_size=10, batch_size=20,
                 name='QNetwork'):
        # state inputs to the Q-network
        with tf.variable_scope(name):
            self.inputs_ = tf.placeholder(tf.float32, [None, state_size], name='inputs')

            # One hot encode the actions to later choose the Q-value for the action
            self.actions_ = tf.placeholder(tf.int32, [batch_size], name='actions')
            #one_hot_actions = tf.one_hot(self.actions_, action_size)

            # Target Q values for training
            #self.targetQs_ = tf.placeholder(tf.float32, [None], name='target')

            # ReLU hidden layers
            self.fc1 = tf.contrib.layers.fully_connected(self.inputs_, hidden_size)
            self.fc2 = tf.contrib.layers.fully_connected(self.fc1, hidden_size)

            # Linear output layer
            self.output = tf.contrib.layers.fully_connected(self.fc2, action_size,
                                                            activation_fn=None)

            self.targetQs_ = tf.placeholder(tf.float32, [batch_size,action_size], name='target')
            self.reward = tf.placeholder(tf.float32,[batch_size],name="reward")
            self.discount = tf.constant(0.99,shape=[batch_size],dtype=tf.float32,name="discount")

            #TRFL qlearning
            qloss, q_learning = trfl.qlearning(self.output,self.actions_,self.reward,self.discount,self.targetQs_)
            self.loss = tf.reduce_mean(qloss)
            self.opt = tf.train.AdamOptimizer(learning_rate).minimize(self.loss)
