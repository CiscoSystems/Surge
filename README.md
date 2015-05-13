# Surge

## License

Copyright 2015 Cisco Systems, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.

Surge is a system to rapidly deploy and scale a stream processing system on OpenStack. It leverages Vagrant and Ansible, and supports both OpenStack as well as the local mode (with VirtualBox).

The currently supported sytems are:

 * Kafka
 * Storm

*Note: This is an alpha status tool. We do not recommend using for production deployments. Please help us by reporting bugs.*

## Requirements

 * Pip
 * Vagrant
 * VirtualBox
 * Ubuntu: python-dev (apt)

## Installation

Install from this repository:

    $ vagrant plugin install vagrant-openstack-provider
    $ pip install virtualenv
    $ virtualenv env
    $ source env/bin/activate
    $ git clone https://github.com/CiscoSystems/Surge.git
    $ pip install -e Surge/
    $ surge deploy Surge/example/pipeline.yml -n KafkaPipeline
    $ surge ssh KafkaPipeline [zookeeper1|kafka1|kafka2]
    $ surge destroy KafkaPipeline

## Usage

To use it:

    $ surge --help

### Create a pipeline file
You can use the file in the `example` folder as a base to configure your pipeline. You should only need to modify the providers' configuration and adjust the number of nodes required for each system.

### Deploy a pipeline to VirtualBox

    $ surge deploy --help
    $ surge deploy path/to/pipeline.yml -n PipelineName

### Deploy a pipeline to OpenStack

    $ surge deploy path/to/pipeline.yml -n PipelineName --openstack

*Note: Some OpenStack environments, mostly Devstack ones, might be slow when booting machines. If the `deploy` operation times out, rerun it again and it will resume where it stopped.*

### See the status of a pipeline

    $ surge status PipelineName

### Ssh into a node

    $ surge ssh PipelineName nodeName

### Destroy a pipeline

    $ surge destroy PipelineName

### Create a template
If you are going to reuse the same pipeline frequently, you can add it as a template

    $ surge create_template path/to/pipeline.yml TemplateName

### Deploy from template

    $ surge deploy_template TemplateName -n PipelineName

### List pipelines

    $ surge list

### List saved templates

    $ surge list_templates
