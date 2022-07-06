from parameterized import parameterized
from parse_tests_yaml import ParseTestData
import subprocess
import unittest

test_data = ParseTestData()
ids = test_data.get_blueprints_ids()
# args = test_data.get_args()
# args_uninstall = test_data.get_args_uninstall()
args_upload = test_data.get_blueprints_args()

class TestBlueprints(unittest.TestCase):
    def upload(self, id):
        for blueprint in ids[:5]: 
            with self.subTest(blueprint):
                proc_upload = subprocess.run(args_upload.get(blueprint))
                self.assertTrue(proc_upload.returncode == 0)
    
    # def install(self):
    #     for blueprint in ids:
    #         with self.subTest(blueprint):
    #             proc_install = subprocess.run(args.get(blueprint))
    #             proc_uninstall = subprocess.run(
    #                 args_uninstall.get(blueprint), timeout=300)
    #             self.assertTrue(proc_install.returncode ==
    #                         0 and proc_uninstall.returncode == 0)

def upload_bps(arg):
    proc_upload = subprocess.run(arg)
    assert proc_upload.returncode == 0

def test_generator():
    for id in ids:
        yield upload_bps, args_upload.get(id)

