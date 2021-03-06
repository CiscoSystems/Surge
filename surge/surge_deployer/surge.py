# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import vagrant
import os
import shutil
from os.path import expanduser

HOME = expanduser("~")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class VagrantDeployer:
    def __init__(self, name, pipeline=None, provider=None):
        self.name = name
        self.path = HOME + '/.surge/' + name

        if not os.path.exists(self.path):
            self._setup_pipeline_env(provider)

        if pipeline is not None:
            print pipeline
            self._set_pipeline(pipeline)
            # self.ansibleManager.createInventory()

        self._get_vagrant()

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
        if os.path.exists(self.path) and os.path.exists(self.path +
                                                        '/pipeline.yml'):
            return True
        return False

    def _get_vagrant(self):
        self.v = vagrant.Vagrant(
            self.path, quiet_stdout=False, quiet_stderr=False)

    def _set_pipeline(self, pipeline):
        shutil.copy(pipeline, self.path + "/pipeline.yml")

    def _setup_pipeline_env(self, provider):
        provider = str(provider)
        if provider == "virtualbox":
            shutil.copytree(BASE_DIR + '/basevb', self.path)
        elif provider == "openstack":
            shutil.copytree(BASE_DIR + '/baseos', self.path)
        else:
            shutil.copytree(BASE_DIR + '/basedocker', self.path)
        # Also copying the playbooks, to ensure deployed pipelines remain
        # manageable in case of a change in the playbooks.
        if provider == "docker":
            shutil.copytree(BASE_DIR + '/surge-docker-playbooks', self.path
                            + '/surge-docker-playbooks')
        else:
            shutil.copytree(BASE_DIR + '/surge-playbooks', self.path
                            + '/surge-playbooks')
