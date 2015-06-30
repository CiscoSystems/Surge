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


"""Tests for surge/surge_deployer/surge.py
"""
import mock
import os
import pytest
import shutil

from surge.surge_deployer.surge import VagrantDeployer


@pytest.fixture
def fake_vd():
    return VagrantDeployer("fake_name")


def test_status(fake_vd):
    with mock.patch.object(VagrantDeployer, '_exists') as fake_exists:
        fake_exists.return_value = True
        with mock.patch.object(VagrantDeployer, '_action') as fake_action:
            fake_vd.status()
            assert len(fake_action.mock_calls) == 1
        fake_exists.return_value = False
        result = fake_vd.status()
        assert result == "Undeployed"


def test_deploy(fake_vd):
    with mock.patch.object(VagrantDeployer, '_action') as fake_action:
        fake_vd.deploy("fake_providor")
        assert len(fake_action.mock_calls) == 1


def test_vagrant(fake_vd):
    # Under the consideration for implementing _vagrant_[up|destroy|status] methods
    # instead of using vagrant method or somehow mocking the self.v attribute.
    pass


def test_setup_pipeline_env(fake_vd):
    with mock.patch.object(shutil, 'copytree') as fake_copytree:
        fake_vd._setup_pipeline_env("virtualbox")
        assert len(fake_copytree.mock_calls) == 2
    with mock.patch.object(shutil, 'copytree') as fake_copytree:
        fake_vd._setup_pipeline_env("openstack")
        assert len(fake_copytree.mock_calls) == 2
    with mock.patch.object(shutil, 'copytree') as fake_copytree:
        fake_vd._setup_pipeline_env("some other things")
        assert len(fake_copytree.mock_calls) == 2


def test_exists(fake_vd):
    with mock.patch.object(os.path, 'exists') as fake_exists:
        fake_exists.return_value = True
        result = fake_vd._exists("fake_name")
        assert result
        fake_exists.return_value = False
        result = fake_vd._exists("fake_name")
        assert result is False


def test_destroy(fake_vd):
    with mock.patch.object(VagrantDeployer, '_exists') as fake_exists:
        with mock.patch.object(shutil, 'rmtree') as fake_rmtree:
            with mock.patch.object(VagrantDeployer, '_action') as fake_action:
                fake_exists.return_value = True
                fake_vd.destroy()
                assert len(fake_action.mock_calls) == 1
                assert len(fake_rmtree.mock_calls) == 1
            fake_exists.return_value = False
            fake_vd.destroy()
            assert len(fake_rmtree.mock_calls) == 2
