#!/usr/bin/env python
# coding: utf-8

from TrainCatan import TrainCatan
import sys

train=None

def pairwise(it):
    it = iter(it)
    while True:
        yield next(it), next(it)

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__":

    train = TrainCatan()

    for param,param_value in pairwise(sys.argv[1:]): #first argument is executed file
        if isint(param_value):
            setattr(train,param,int(param_value))
        elif isfloat(param_value):
            setattr(train,param,float(param_value))
        else:
            setattr(train,param,param_value)

    train.start_training()


