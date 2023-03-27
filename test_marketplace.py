import os
import subprocess
import logging

import pytest
from pytest_steps import test_steps

from parse_tests import ParseTestData

BPS_SCOPE = os.environ.get('BPS_SCOPE')

test_data = ParseTestData(BPS_SCOPE)
ids = test_data.get_blueprints_ids()
# upload
args_upload = test_data.get_upload_args()
# install
args_create_deployment = test_data.get_create_deployment_args()
args_executions_start = test_data.get_executions_start_args()
args_uninstall = test_data.get_uninstall_args()

# single_blueprint
single_blueprint = [os.environ.get('TEST_BLUEPRINT')]


@pytest.mark.single_upload
@pytest.mark.parametrize("id", single_blueprint)
def test_single_upload(id):
    if id:
        if not id in args_upload.keys():
            exit(-1)
        test_upload(id)
    else:
        raise Exception("Invalid blueprint_id")


@pytest.mark.upload
@pytest.mark.parametrize("id", args_upload.keys())
def test_upload(id):
    proc = subprocess.run(args_upload.get(id), stdout=subprocess.PIPE)
    assert proc.returncode == 0, proc.stdout


@pytest.mark.install
@test_steps("create_deployment", "install_deployment", "uninstall_deployment")
@pytest.mark.parametrize("id", args_executions_start.keys())
def test_install(id):
    # assuming that install & update could be run separetely
    try:
        upload_bp = subprocess.run(args_upload.get(id), stdout=subprocess.PIPE)
        logging.info(upload_bp.stdout)
    except Exception as err:
        logging.error(err)
    try:
        create_deployment = subprocess.run(
            args_create_deployment.get(id), stdout=subprocess.PIPE)
        assert create_deployment.returncode == 0, create_deployment.stdout
        yield
        executions_start = subprocess.run(
            args_executions_start.get(id), stdout=subprocess.PIPE, timeout=900)
        assert executions_start.returncode == 0, executions_start.stdout
        yield
    finally:
        uninstall_start = subprocess.run(
            args_uninstall.get(id), stdout=subprocess.PIPE)
        assert uninstall_start.returncode == 0, uninstall_start.stdout
        yield


@pytest.mark.single_install
@pytest.mark.parametrize("id", single_blueprint)
def test_single_install(id):
    if id:
        if not id in args_upload.keys():
            exit(-1)
        test_install(id)
    else:
        raise Exception("Invalid blueprint_id")
