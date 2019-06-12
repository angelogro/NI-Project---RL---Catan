#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
import sys

train=None

def pairwise(it):
    it = iter(it)
    while True:
        yield next(it), next(it)

if __name__ == "__main__":

    train = TrainCatan()

    for param,param_value in pairwise(sys.argv[1:]): #first argument is executed file
        if isinstance(param_value,int):
            setattr(train,param,int(param_value))
        elif isinstance(param_value,float):
            setattr(train,param,float(param_value))
        else:
            setattr(train,param,param_value)

    train.start_training()


