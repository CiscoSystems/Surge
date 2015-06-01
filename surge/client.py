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


class SurgeClient:

    def launch_kafka(self, pipeline_name, brokers):
        deployer = VagrantDeployer(pipeline_name)
        surge_utils.generate_kafka_component(pipeline_name, brokers)
        deployer.deploy("virtualbox")

    def launch_storm(self, pipeline_name, supervisors):
        deployer = VagrantDeployer(pipeline_name)
        surge_utils.generate_storm_component(pipeline_name, supervisors)
        deployer.deploy("virtualbox")

    def list_pipeline(self):
        return surge_utils.list_pipelines()

    def destroy_pipeline(self, pipeline_name):
        deployer = VagrantDeployer(pipeline_name)
        deployer.destroy()
