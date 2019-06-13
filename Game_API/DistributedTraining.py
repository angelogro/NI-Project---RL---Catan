from TrainCatan import TrainCatan
from GcloudInstance import GcloudInstance
from itertools import product
import subprocess
import os
import sys
import time
import pickle
from shutil import copyfile

INSTANCES_FOLDER = 'instance_parameters'

class DistributedTraining():

    def __init__(self,instances_name_base,param_dic):

        self.g_cloud_instances = []

        assert type(param_dic) == dict
        self.t = TrainCatan()
        for param in param_dic:
            if not hasattr(self.t, param):
                print('TrainCatan has no attribute named '+param)
                sys.exit()


        list_combinations = [dict(zip(param_dic, v)) for v in product(*param_dic.values())]
        counter = 0
        for param_combination in list_combinations:

            instance_name = instances_name_base+str(counter)
            self.create_startup_script(instance_name,param_combination)
            self.g_cloud_instances.append(GcloudInstance(instance_name,param_combination))
            self.g_cloud_instances[-1].start_instance()
            counter+=1

        self.outstanding_instance_files = [instance.instance_name for instance in self.g_cloud_instances]

    def start_instances(self):
        for instance in self.g_cloud_instances:
            instance.start_instance()

    def delete_instances(self):
        for instance in self.g_cloud_instances:
            instance.remove_instance()

    def create_startup_script(self,instance_name,param_combination):
        param_value_string = ''.join([' ',instance_name])
        for param in param_combination:
            param_value_string = ''.join([param_value_string,' ',param,' '])

            if isinstance(param_combination[param],tuple):
                param_value_string = ''.join([param_value_string,str('\''),str(param_combination[param]),str('\'')])
            else:
                param_value_string = ''.join([param_value_string,str(param_combination[param])])

        copyfile('../startup_script_template.sh', '../startup_script.sh')
        with open('../startup_script.sh','rb+') as f: #open in binary mode
            f.seek(-1,2) #move to last char of file
            f.write(param_value_string.encode())
            f.close()
        print(param_value_string)

    def request_hyperparameter_files_from_instances(self):
        """
        Request all instance information including victory curves from the instance.

        If available, the files are sent to the host machine in the folder specified
        by the variable INSTANCES_FOLDER.
        The syntax for the gcloud command which is executed can be found under
        https://cloud.google.com/sdk/gcloud/reference/compute/scp.
        """

        if not os.path.exists(INSTANCES_FOLDER):
            os.mkdir(INSTANCES_FOLDER)

        while(len(self.outstanding_instance_files) > 0):
            time.sleep(30)
            print(''.join([str(self.outstanding_instance_files),' still not obtained.']))
            for instance in self.g_cloud_instances:

                if instance.instance_name in self.outstanding_instance_files:
                    return_value = subprocess.call(["gcloud", "compute" ,"scp","--zone","europe-west1-b", ''.join([instance.instance_name,':/catan/NI-Project---RL---Catan/Game_API/hyperparameters/',instance.instance_name,'/',instance.instance_name])
                                            ,os.path.join(os.path.dirname(os.path.abspath(__file__)),''.join([INSTANCES_FOLDER,'/',instance.instance_name]))],
                                        executable='/home/angelo/Downloads/google-cloud-sdk/bin/gcloud')
                    if return_value == 0:
                        print(''.join([instance.instance_name,' finished.']))
                        self.outstanding_instance_files.remove(instance.instance_name)

                if len(self.outstanding_instance_files) == 0:
                    print('Obtained all hyperparameter files.')
                    break


    def show_instances_graphs(self):
        plot_counter = 0
        for instance in self.g_cloud_instances:
            t_i = self.load_hyperparameters(instance.instance_name)
            t_i.autosave = False
            t_i.init_online_plot(instance.instance_name,plot_counter)
            t_i.plot_statistics_online(t_i.victories,t_i.epsilons,t_i.cards,t_i.one_of_training_instances_wins,t_i.learning_rates,t_i.plot_interval)
            plot_counter+=1


    def load_hyperparameters(self,filename):
        if not os.path.isfile(''.join([INSTANCES_FOLDER,'/',filename])):
            return
        f = open(''.join([INSTANCES_FOLDER,'/',filename]), 'rb')
        return pickle.load(f)