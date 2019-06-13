from TrainCatan import TrainCatan
from GcloudInstance import GcloudInstance
from itertools import product
import subprocess
import os
import sys
from shutil import copyfile

class DistributedTraining():

    def __init__(self,param_dic):

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
            instance_name = 'b'+str(counter)
            self.create_startup_script(instance_name,param_combination)
            self.g_cloud_instances.append(GcloudInstance(instance_name,param_combination))
            counter+=1

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
                param_value_string = ''.join([param_value_string,param_combination[param]])

        copyfile('../startup_script_template.sh', '../startup_script.sh')
        with open('../startup_script.sh','rb+') as f: #open in binary mode
            f.seek(-1,2) #move to last char of file
            f.write(param_value_string.encode())
            f.close()
        print(param_value_string)

    def request_hyperparameter_files_from_instances(self):
        folder_name = 'instance_parameters'
        os.mkdir(folder_name)

        for instance in self.g_cloud_instances:
            try:
                subprocess.call(["gcloud", "compute" ,"scp","--zone","europe-west1-b", ''.join([instance.instance_name,'/catan/NI-Project---RL---Catan/Game_API/hyperparameters/',instance.instance_name,'/',instance.instance_name])
                                    ,os.path.join(os.path.dirname(os.path.abspath(__file__)),''.join[folder_name,'/',instance.instance_name])],
                            executable='/home/angelo/Downloads/google-cloud-sdk/bin/gcloud')
            except:
                pass
