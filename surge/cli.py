

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

import click
from surge_deployer import surge
import os
import shutil

CLI_BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, debug):
    """Surge command line client"""
    ctx.obj['DEBUG'] = debug
    if debug:
        click.echo("Starting Surge in DEBUG mode")


@main.command()
@click.argument('filename', required=True)
@click.option('--name', '-n', required=True)
@click.option('--virtualbox', 'provider', flag_value='virtualbox', default=True)
@click.option('--openstack', 'provider', flag_value='openstack')
@click.option('--docker', 'provider', flag_value='docker')
@click.pass_context
def deploy(ctx, filename, name, provider):
    """Deploy a new pipeline"""
    if (ctx.obj['DEBUG']):
        print("Pipeline filename: " + filename)
        print("Provider: " + provider)
    # Creating ansible inventory file
    # create_ansible_inventory(ctx, filename, provider)
    click.echo('Checking pipeline...')

    v = surge.VagrantDeployer(name, filename, provider)
    v.deploy(provider)


@main.command()
@click.argument('name', required=True)
@click.pass_context
def provision(ctx, name):
    """Run provisioning on a pipeline"""

    v = surge.VagrantDeployer(name)
    v.provision()


@main.command()
@click.argument('template', required=True)
@click.option('--name', '-n', required=True)
@click.option('--virtualbox', 'provider', flag_value='virtualbox', default=True)
@click.option('--openstack', 'provider', flag_value='openstack')
@click.option('--docker', 'provider', flag_value='docker')
@click.pass_context
def deploy_template(ctx, template, name, provider):
    """Deploy a pipeline from a template"""
    if (ctx.obj['DEBUG']):
        print("Pipeline filename: " + name)
    print("Provider: " + provider)
    # Creating ansible inventory file
    # create_ansible_inventory(ctx, filename, provider)
    p = os.listdir(CLI_BASE_DIR + '/surge_deployer/templates')
    if template in p:
        v = surge.VagrantDeployer(
            name, CLI_BASE_DIR + '/surge_deployer/templates/' + template + "/pipeline.yml", provider)
        print(provider)
        v.deploy(provider)
    else:
        click.echo("Unknown provider")


@main.command()
@click.argument('filename', required=True)
@click.argument('name', required=True)
@click.pass_context
def create_template(ctx, filename, name):
    """Create a template from a pipeline file"""
    path = CLI_BASE_DIR + '/surge_deployer/templates/' + name
    if not os.path.exists(path):
        os.makedirs(path)
    shutil.copy(filename, path + "/pipeline.yml")
    click.echo(
        "Template added. Please deploy it by running surge deploy-template " + name)


@main.command()
@click.pass_context
def list_templates(ctx):
    """List all available templates"""
    templates_dir = CLI_BASE_DIR + '/surge_deployer/templates'
    if not os.path.exists(templates_dir):
        click.echo("No templates available: %s does not exist" % templates_dir)
        return
    p = os.listdir(templates_dir)
    if len(p) is 0:
        click.echo("No templates available")
    else:
        click.echo("\n".join(p))


@main.command()
@click.argument('name', required=True)
@click.pass_context
def destroy(ctx, name):
    """Destroy a deployed pipeline"""
    # Creating ansible inventory file
    # create_ansible_inventory(ctx, filename, provider)
    click.echo('Checking pipeline...')

    v = surge.VagrantDeployer(name)
    v.destroy()


@main.command()
@click.argument('name', required=True)
@click.pass_context
def status(ctx, name):
    """Check status of a pipeline"""
    click.echo('Checking status...')

    v = surge.VagrantDeployer(name)
    print(v.status())


@main.command()
@click.pass_context
def list(ctx):
    """List currently deployed pipelines"""
    p = os.listdir(CLI_BASE_DIR + '/surge_deployer/pipelines')
    if len(p) is 0:
        click.echo("No deployed pipelines")
    else:
        click.echo("\n".join(p))


@main.command()
@click.argument('name', required=True)
@click.argument('vmname', required=True)
@click.pass_context
def ssh(ctx, name, vmname):
    """SSH into an instance"""
    click.echo('Checking status...')
    v = surge.VagrantDeployer(name)
    a = v.ssh(vmname).split("\n")
    a = map(lambda x: x.strip(), a)
    data = {}
    for i in a:
        e = i.split(" ")
        if len(e) == 2:
            data[e[0]] = e[1]
    hostname = data["HostName"]
    user = data['User']
    port = data['Port']
    key = data['IdentityFile']
    _ssh(user, hostname, port, key)


def _ssh(user, hostname, port, key):
    os.system('ssh ' + user + '@' + hostname + ' -p' + port +
              ' -i ' + key + ' -o StrictHostKeyChecking=no')


def cli():
    return main(obj={})
