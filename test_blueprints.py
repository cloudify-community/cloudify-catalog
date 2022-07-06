from parse_tests_yaml import ParseTestData
import subprocess
from nose.plugins.attrib import attr
import unittest

test_data = ParseTestData()
ids = test_data.get_blueprints_ids()
# args = test_data.get_args()
# args_uninstall = test_data.get_args_uninstall()
args_upload = test_data.get_blueprints_args()

@attr(type="upload")
class TestBlueprints:
    def upload_bp(self, arg):
        proc_upload = subprocess.run(arg)
        assert proc_upload.returncode == 0

    def test_uploads(self):
        for id in ids:
            yield self.upload_bp, args_upload.get(id)
    
    # def install(self):
    #     for blueprint in ids:
    #         with self.subTest(blueprint):
    #             proc_install = subprocess.run(args.get(blueprint))
    #             proc_uninstall = subprocess.run(
    #                 args_uninstall.get(blueprint), timeout=300)
    #             self.assertTrue(proc_install.returncode ==
    #                         0 and proc_uninstall.returncode == 0)



