#!/bin/bash

sudo apt update -y
sudo apt install python python-dev python3 python3-dev -y

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pip install --upgrade virtualenv 

mkdir catan
cd catan

virtualenv --python python3 env
source env/bin/activate

pip install numpy
pip install scipy
pip install tensorflow
pip install matplotlib
pip install datetime

sudo apt install git -y

sudo git clone -b TestingWithMultiplePlayerTraining --single-branch https://github.com/angelogro/NI-Project---RL---Catan.git

cd NI-Project---RL---Catan/Game_API/

sudo python run_this.py










