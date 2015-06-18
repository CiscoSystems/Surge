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

from surge.surge_deployer.surge import VagrantDeployer
import surge.surge_deployer.utils as surge_utils


class SurgeAPI:
    """
    Provide Surge functionality to external usage.
    """

    def launch_kafka(self, pipeline_name, brokers):
        """ Launching Apache Kafka
        :param pipeline_name: the identifier of the pipeline
        :param brokers: the number of kafka brokers
        :return: none. (should be status or exception)
        """
        deployer = VagrantDeployer(pipeline_name)
        surge_utils.generate_kafka_component(pipeline_name, brokers)
        deployer.deploy("virtualbox")

    def launch_storm(self, pipeline_name, supervisors):
        """ Launching Apache Storm
        :param pipeline_name: the identifier of the pipeline
        :param supervisors: the number of supervisor nodes
        :return: none. (should be status or exception)
        """
        deployer = VagrantDeployer(pipeline_name)
        surge_utils.generate_storm_component(pipeline_name, supervisors)
        deployer.deploy("virtualbox")

    def list_pipeline(self):
        """ List existing pipelines
        :return: the list of current pipelines
        """
        return surge_utils.list_pipelines()

    def destroy_pipeline(self, pipeline_name):
        """ Destroying pipeline
        :param pipeline_name: the target pipeline
        :return: none. (should be status)
        """
        deployer = VagrantDeployer(pipeline_name)
        deployer.destroy()

    def provision_pipeline(self, pipeline_name):
        """ Provisioning pipeline
        :param pipeline_name: the identifire of the pipeline
        :return: none. (should be status)
        """
        deployer = VagrantDeployer(pipeline_name)
        deployer.provision()
