# NI-Project---RL---Catan
University project, developing an Agent which learns playing the Catan board game (https://www.catan.com/game/catan)

<!-- Bild vom Board oder Ähnliches hinzufügen -->
![CatanBoard]()
## Getting started 
1. Clone repository 
2. Install all dependencies

    ```
    pip install -r requirements.txt
    ```

## Usage
In order to train or play with the agent use: 
```
run_this.py
```

### run_this.py
run_this.py imports the following modules and their respective classes:

* agent.traincatan
* agent.distributedtraining

#### TrainCatan
To start training create an object TrainCatan with desired parameters.
The list of parameters / attributes and functions can be seen in the module TrainCatan. 
[Link to list of attributes](https://github.com/angelogro/NI-Project---RL---Catan/blob/4e40bd5dd3f1c343d7866b5c2811d8f333189049/catan/agent/traincatan.py#L17-L88)
[Link to list of functions](https://github.com/angelogro/NI-Project---RL---Catan/blob/4e40bd5dd3f1c343d7866b5c2811d8f333189049/catan/agent/traincatan.py#L91-L120)



#### DistributedTraining
When creating the object from class DistributedTraining,
the amount of vectors of hyperparameters are used to create a set of hyperparameter combinations by means of the cartesian product. GCloud instances are launched with each element of that set.
![DistributedTraining]()


