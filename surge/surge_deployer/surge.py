import vagrant
import os
import shutil

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
            self._set_pipeline(pipeline)
            # self.ansibleManager.createInventory()

        self.v = vagrant.Vagrant(
            self.path, quiet_stdout=False, quiet_stderr=False)

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

    def deploy(self, provider):
        print("Deploying with provider: " + provider)
        return self._action("up", provider=provider)

    def provision(self):
        return self._action("provision")

    def status(self):
        if self._exists(self.name):
            return self._action("status")
        else:
            return "Undeployed"

    def ssh(self, vmname):
        return self.v.ssh_config(vm_name=vmname)

    def destroy(self):
        if self._exists(self.name):
            self._action("destroy")
        shutil.rmtree(self.path)

    def _action(self, action, provider="virtualbox"):
        return self.vagrant(action, provider)

    def _exists(self, name):
        if os.path.exists(self.path) and os.path.exists(self.path + '/pipeline.yml'):
            return True
        return False

    def _set_pipeline(self, pipeline):
        shutil.copy(pipeline, self.path + "/pipeline.yml")
