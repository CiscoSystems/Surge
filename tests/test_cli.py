

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


""" Tests for surge/cli.py
"""
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


def test_cli_provision(runner):
    with mock.patch.object(VagrantDeployer, 'provision') as fake_prvision:
        result = runner.invoke(cli.provision, ["fake_name"])
        assert len(fake_prvision.mock_calls) == 1
        assert result.exit_code == 0

    # exit code should be not 0 when it failures
    result = runner.invoke(cli.provision, ["name"])
    assert result.exit_code != 0


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
