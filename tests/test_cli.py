""" Tests for surge/cli.py
"""
import shutil
import pytest
import os
import mock
from click.testing import CliRunner

from surge import cli
from surge.surge_deployer.surge import VagrantDeployer


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_main(runner):
    with mock.patch.object(cli, 'main') as fake_main:
        cli.cli()
        assert len(fake_main.mock_calls) == 1

    # exit code should be not 0 when it failures
    result = runner.invoke(cli.main, ["hogehoge123"])
    assert result.exit_code != 0


def test_cli_deploy(runner):
    with mock.patch.object(VagrantDeployer, '_get_vagrant') as fake_get_vagrant:
        with mock.patch.object(VagrantDeployer, 'deploy') as fake_deploy:
            result = runner.invoke(cli.deploy, ['fake_filename', 'fake_name', 'virtualbox'])
            assert len(fake_deploy.mock_calls) == 1
            assert len(fake_get_vagrant.mock_calls) == 1
            assert result.exit_code == 0


def test_cli_provision(runner):
    with mock.patch.object(VagrantDeployer, 'provision') as fake_prvision:
        result = runner.invoke(cli.provision, ["fake_name"])
        assert len(fake_prvision.mock_calls) == 1
        assert result.exit_code == 0

    # exit code should be not 0 when it failures
    result = runner.invoke(cli.provision, ["name"])
    assert result.exit_code != 0


def test_deploy_template(runner):
    with mock.patch.object(os, 'listdir') as fake_listdir:
        fake_listdir.return_value = ["fake_template"]
        with mock.patch.object(VagrantDeployer, '_get_vagrant') as fake_get_vagrant:
            with mock.patch.object(VagrantDeployer, 'deploy') as fake_deploy:
                result = runner.invoke(cli.deploy_template, ["fake_filename", "fake_name", "virtualbox"])
                assert len(fake_get_vagrant.mock_calls) == 1
                assert len(fake_deploy.mock_calls) == 1
                assert result.exit_code == 0
        fake_listdir.return_value = []
        result = runner.invoke(cli.deploy_template, ["fake_filename", "fake_name", "virtualbox"])
        assert result.exit_code == 0


def test_cli_create_template(runner, tmpdir):
    with runner.isolated_filesystem():
        with mock.patch.object(shutil, 'copy') as fake_copy:
            result = runner.invoke(cli.create_template, ["fake_filename", "fake_name"])
            assert len(fake_copy.mock_calls) == 1
            assert result.exit_code == 0
        cli.CLI_BASE_DIR = str(tmpdir)
        tmpdir.mkdir('surge_deployer').mkdir('templates')
        result = runner.invoke(cli.create_template, ["fake_filename", "fake_name"])
        assert result.exit_code == 0


def test_cli_list_template(runner):
    with mock.patch.object(os.path, 'exists') as fake_exist:
        fake_exist.return_value = False
        result = runner.invoke(cli.list_templates)
        assert result.exit_code == 0
        fake_exist.return_value = True
        with mock.patch.object(os, 'listdir') as fake_listdir:
            fake_listdir.return_value = ['fake_dif']
            result = runner.invoke(cli.list_templates)
            assert result.exit_code == 0
            fake_listdir.return_value = []
            result = runner.invoke(cli.list_templates)
            assert result.exit_code == 0


def test_cli_destroy(runner):
    with mock.patch.object(VagrantDeployer, '_get_vagrant') as fake_get_vagrant:
        with mock.patch.object(VagrantDeployer, 'destroy') as fake_destroy:
            result = runner.invoke(cli.destroy, ["fake_name"])
            assert len(fake_get_vagrant.mock_calls) == 1
            assert len(fake_destroy.mock_calls) == 1
            assert result.exit_code == 0

    # exit code should be not 0 when it failures
    result = runner.invoke(cli.destroy, ["fake_name"])
    assert result.exit_code == 0


def test_cli_status(runner):
    with mock.patch.object(VagrantDeployer, '_get_vagrant') as fake_get_vagrant:
        with mock.patch.object(VagrantDeployer, 'status') as fake_status:
            result = runner.invoke(cli.status, ["fake_name"])
            assert len(fake_get_vagrant.mock_calls) == 1
            assert len(fake_status.mock_calls) == 2
            assert result.exit_code == 0

    # surge status [name] command return 0 at anytime
    result = runner.invoke(cli.status, ["fake_name"])
    assert result.exit_code == 0


def test_cli_list_with_template(runner):
    with mock.patch.object(os, 'listdir') as fake_listdir:
        fake_listdir.return_value = ['']
        result = runner.invoke(cli.list)
        assert result.exit_code == 0
        fake_listdir.return_value = ['fake_template']
        result = runner.invoke(cli.list)
        assert result.exit_code == 0


def test_cli_ssh_with_non_exist_name(runner):
    result = runner.invoke(cli.ssh, ["fake_name", "fake_vname"])
    assert result.exit_code != 0


def test_cli_private_ssh():
    with mock.patch.object(os, 'system') as fake_private_ssh:
        cli._ssh('fake_user', 'fake_hostname', 'fake_port', 'fake_key')
        assert len(fake_private_ssh.mock_calls) == 1


def test_cli_ssh_with_exist_name(runner):
    with mock.patch.object(VagrantDeployer, '_get_vagrant') as fake_get_vagrant:
        with mock.patch.object(VagrantDeployer, 'ssh') as fake_ssh:
            with mock.patch.object(cli, '_ssh') as fake_cli_ssh:
                result = runner.invoke(cli.ssh, ["fake_name", "fake_vname"])
                assert len(fake_get_vagrant.mock_calls) == 1
                assert len(fake_ssh.mock_calls) == 1
                assert len(fake_cli_ssh.mock_calls) == 1
                assert result.exit_code == 0
