import pytest
from parse_tests_yaml import ParseTestData

import subprocess

test_data = ParseTestData()
ids = test_data.get_blueprints_ids()
args_upload = test_data.get_upload_args()
args_create_deployment = test_data.get_create_deployment_args()
args_executions_start = test_data.get_executions_start_args()
args_uninstall = test_data.get_uninstall_args()

@pytest.mark.parametrize("id", list(args_upload.keys())[:3])
def test_upload(id):
    proc = subprocess.run(args_upload.get(id), stdout=subprocess.PIPE)
    assert proc.returncode == 0, proc.stdout

@pytest.mark.parametrize("id", args_executions_start.keys())
def test_install(id):
    create_deployment = subprocess.run(args_create_deployment.get(id), stdout = subprocess.PIPE)
    assert create_deployment.returncode == 0, create_deployment.stdout
    executions_start = subprocess.run(args_executions_start.get(id), stdout=subprocess.PIPE)
    assert executions_start.returncode == 0, executions_start.stdout
    uninstall_start = subprocess.run(args_uninstall.get(id), stdout=subprocess.PIPE)
    assert uninstall_start.returncode == 0, uninstall_start.stdout