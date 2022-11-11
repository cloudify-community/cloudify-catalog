from unittest import TestCase
from parse_tests_yaml import ParseTestData
import subprocess

test_data = ParseTestData()
ids = test_data.get_blueprints_ids()
#args = test_data.get_install_args()
#args_uninstall = test_data.get_args_uninstall()
args_upload = test_data.get_upload_args()

def test_always_passes():
    for arg in args_upload: 
        proc_upload = subprocess.run(arg)
        break
    assert proc_upload.returncode == 0