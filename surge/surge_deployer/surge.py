import vagrant
import sys
import StringIO
import time
import os
import shutil
import ansible

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class VagrantDeployer:

    def __init__(self, name, pipeline=None, provider=None):
        self.name = name
        self.path = BASE_DIR + '/pipelines/' + name

        if not os.path.exists(self.path):
            if provider is "virtualbox":
                shutil.copytree(
                    BASE_DIR + '/basevb', self.path)
            elif provider is "openstack":
                shutil.copytree(
                    BASE_DIR + '/baseos', self.path)
            else:
                shutil.copytree(
                    BASE_DIR + '/basedocker', self.path)

        if pipeline is not None:
            print pipeline
            self.setPipeline(pipeline)
            # self.ansibleManager.createInventory()

        self.v = vagrant.Vagrant(
            self.path, quiet_stdout=False, quiet_stderr=False)

    def exists(self, name):
        if os.path.exists(self.path) and os.path.exists(self.path + '/pipeline.yml'):
            return True
        return False

    def setPipeline(self, pipeline):
        shutil.copy(pipeline, self.path + "/pipeline.yml")

    def vagrant(self, action, provider="virtualbox"):
        if action is 'up':
            print(provider)
            return self.v.up(provider=provider)
        elif action is 'destroy':
            return self.v.destroy()
        elif action is "status":
            return self.v.status()
        else:
            return self.v.provision()

    def action(self, action, provider="virtualbox"):
        return self.vagrant(action, provider)

    def deploy(self, provider):
        print("Deploying with provider: " + provider)
        return self.action("up", provider=provider)

    def provision(self):
        return self.action("provision")

    def status(self):
        if self.exists(self.name):
            return self.action("status")
        else:
            return "Undeployed"

    def ssh(self, vmname):
        return self.v.ssh_config(vm_name=vmname)

    def destroy(self):
        if self.exists(self.name):
            self.action("destroy")
        shutil.rmtree(self.path)