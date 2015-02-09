# Surge

Surge is a tool working on top of Vagrant and using Ansible, aiming to let you easily deploy and scale data stream processing systems both locally or to an OpenStack Cluster.

The currently supported sytems are:

 * Kafka
 * Storm

*Note: This is an alpha status tool. We do not recommend using for production deployments. Please help us by reporting bugs.*

## Requirements

 * Pip
 * Vagrant
 * vagrant-openstack-provider
 * VirtualBox

## Installation

Install from this repository:

    $ pip install virtualenv
    $ virtualenv env
    $ source env/bin/activate
    $ git clone https://github.com/CiscoSystems/Surge.git
    $ pip install -e Surge/

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

### See the status of a pipeline

    $ surge status PipelineName

### Ssh into a node

    $ surge ssh nodeName

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