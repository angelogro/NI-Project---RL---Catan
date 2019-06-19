#!/bin/bash

sudo apt update -y

#install dependencies for python 3.6
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y

#install python 3.6.3
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
tar -xvf Python-3.6.3.tgz
cd Python-3.6.3

sudo apt install gcc make -y
sudo apt-get install zlib1g-dev
sudo ./configure
sudo make
sudo make install

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pip3 install numpy
sudo pip3 install scipy
sudo pip3 install tensorflow
sudo pip3 install matplotlib
sudo pip3 install datetime

cd /
sudo mkdir catan
cd catan

sudo apt install git -y

sudo git clone -b TestingWithMultiplePlayerTraining --single-branch https://github.com/angelogro/NI-Project---RL---Catan.git

sudo chmod -R 777 *

cd NI-Project---RL---Catan/Game_API/


sudo python3 instance_exe.py learningrate31 num_games 15000 random_init True reward building learning_rate_decay_factor 0.999 learning_rate 0.01 random_shuffle_training_players_ True needed_victory_points 4 replace_target_iter 100 verbose False sigmoid_001_099_borders '(-1000, 11000)' batch_size 4096 learning_rate_start_decay 8000