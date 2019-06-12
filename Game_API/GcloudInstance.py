import argparse
import os
import time

import googleapiclient.discovery
from six.moves import input

class GcloudInstance():
    def __init__(self,instance_name,params):
        self.instance_name = instance_name
        self.params = params
        pass

    # [START list_instances]
    def list_instances(self,compute, project, zone):
        result = compute.instances().list(project=project, zone=zone).execute()
        return result['items'] if 'items' in result else None
    # [END list_instances]


    # [START create_instance]
    def create_instance(self,compute, project, zone, name, bucket):
        # Get the latest Debian Jessie image.
        image_response = compute.images().getFromFamily(
            project='debian-cloud', family='debian-9').execute()
        source_disk_image = image_response['selfLink']

        # Configure the machine
        machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
        startup_script = open(
            os.path.join(
                os.path.dirname(__file__), '../startup_script.sh'), 'r').read()
        image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
        image_caption = "Ready for dessert?"

        config = {
            'name': name,
            'machineType': machine_type,

            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': source_disk_image,
                    }
                }
            ],

            # Specify a network interface with NAT to access the public
            # internet.
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            # Allow the instance to access cloud storage and logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/devstorage.read_write',
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }],

            # Metadata is readable from the instance and allows you to
            # pass configuration from deployment scripts to instances.
            'metadata': {
                'items': [{
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    'key': 'startup-script',
                    'value': startup_script
                }, {
                    'key': 'url',
                    'value': image_url
                }, {
                    'key': 'text',
                    'value': image_caption
                }, {
                    'key': 'bucket',
                    'value': bucket
                }]
            }
        }

        return compute.instances().insert(
            project=project,
            zone=zone,
            body=config).execute()
    # [END create_instance]


    # [START delete_instance]
    def delete_instance(self,compute, project, zone, name):
        return compute.instances().delete(
            project=project,
            zone=zone,
            instance=name).execute()
    # [END delete_instance]


    # [START wait_for_operation]
    def wait_for_operation(self,compute, project, zone, operation):
        print('Waiting for operation to finish...')
        while True:
            result = compute.zoneOperations().get(
                project=project,
                zone=zone,
                operation=operation).execute()

            if result['status'] == 'DONE':
                print("done.")
                if 'error' in result:
                    raise Exception(result['error'])
                return result

            time.sleep(1)
    # [END wait_for_operation]

    def start_instance(self):
        compute = googleapiclient.discovery.build('compute', 'v1')
        operation = self.create_instance(compute, 'settlers', 'europe-west1-b', self.instance_name, 'settlers')

    def remove_instance(self):
        compute = googleapiclient.discovery.build('compute', 'v1')
        operation = self.delete_instance(compute, 'settlers', 'europe-west1-b', self.instance_name)
