from TrainCatan import TrainCatan
from GcloudInstance import GcloudInstance
from itertools import product
import datetime
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
            self.create_startup_script(param_combination)
            self.g_cloud_instances.append(GcloudInstance('a'+str(counter),param_combination))
            counter+=1

    def start_instances(self):
        for instance in self.g_cloud_instances:
            instance.start_instance()

    def delete_instances(self):
        for instance in self.g_cloud_instances:
            instance.remove_instance()

    def create_startup_script(self,param_combination):
        param_value_string = ''
        for param in param_combination:
            param_value_string+=' '
            param_value_string+=param
            param_value_string+=' '
            param_value_string+=str(param_combination[param])

        copyfile('../startup_script_template.sh', '../startup_script.sh')
        f = open('../startup_script.sh','rb+') #open in binary mode
        f.seek(-1,2) #move to last char of file
        f.write(param_value_string.encode())
        f.close()
