import click
from surge_deployer import surge
import os
import shutil


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
@click.option('--virtualbox', 'provider', flag_value='virtualbox',
              default=True)
@click.option('--openstack', 'provider', flag_value='openstack')
@click.pass_context
def deploy(ctx, filename, name, provider):
    """Surge command line client"""
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
    """Surge command line client"""

    v = surge.VagrantDeployer(name)
    v.provision()


@main.command()
@click.argument('template', required=True)
@click.option('--name', '-n', required=True)
@click.option('--virtualbox', 'provider', flag_value='virtualbox',
              default=True)
@click.option('--openstack', 'provider', flag_value='openstack')
@click.pass_context
def deploy_template(ctx, template, name, provider):
    """Surge command line client"""
    if (ctx.obj['DEBUG']):
        print("Pipeline filename: " + filename)
    print("Provider: " + provider)
    # Creating ansible inventory file
    # create_ansible_inventory(ctx, filename, provider)
    p = os.listdir(
        os.path.dirname(os.path.realpath(__file__)) + '/surge_deployer/templates')
    if template in p:
        v = surge.VagrantDeployer(name, os.path.dirname(os.path.realpath(
            __file__)) + '/surge_deployer/templates/' + template + "/pipeline.yml", provider)
        print(provider)
        v.deploy(provider)
    else:
        click.echo("Unknown provider")


@main.command()
@click.argument('filename', required=True)
@click.argument('name', required=True)
@click.pass_context
def create_template(ctx, filename, name):
    """Surge command line client"""
    path = os.path.dirname(
        os.path.realpath(__file__)) + '/surge_deployer/templates/' + name
    if not os.path.exists(path):
        os.makedirs(path)
    shutil.copy(filename, path + "/pipeline.yml")
    click.echo(
        "Template added. Please deploy it by running surge deploy-template " + name)


@main.command()
@click.pass_context
def list_templates(ctx):
    """Surge command line client"""
    p = os.listdir(
        os.path.dirname(os.path.realpath(__file__)) + '/surge_deployer/templates')
    if len(p) is 0:
        click.echo("No templates available")
    else:
        click.echo("\n".join(p))


@main.command()
@click.argument('name', required=True)
@click.pass_context
def destroy(ctx, name):
    """Surge command line client"""
    # Creating ansible inventory file
    # create_ansible_inventory(ctx, filename, provider)
    click.echo('Checking pipeline...')

    v = surge.VagrantDeployer(name)
    v.destroy()


@main.command()
@click.argument('name', required=True)
@click.pass_context
def status(ctx, name):
    """Surge command line client"""
    click.echo('Checking status...')

    v = surge.VagrantDeployer(name)
    print(v.status())


@main.command()
@click.pass_context
def list(ctx):
    """Surge command line client"""
    p = os.listdir(
        os.path.dirname(os.path.realpath(__file__)) + '/surge_deployer/pipelines')
    if len(p) is 0:
        click.echo("No deployed pipelines")
    else:
        click.echo("\n".join(p))


@main.command()
@click.argument('name', required=True)
@click.argument('vmname', required=True)
@click.pass_context
def ssh(ctx, name, vmname):
    """Surge command line client"""
    click.echo('Checking status...')
    v = surge.VagrantDeployer(name)
    a = v.ssh(vmname).split("\n")
    a = map(lambda x: x.strip(), a)
    hostname = a[2].split(' ')[1]
    user = a[3].split(' ')[1]
    port = a[4].split(' ')[1]
    key = a[8].split(' ')[1]
    os.system('ssh ' + user + '@' + hostname + ' -p' + port +
              ' -i ' + key + ' -o StrictHostKeyChecking=no')


def cli():
    return main(obj={})
