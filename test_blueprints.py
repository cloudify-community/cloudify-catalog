from parse_tests_yaml import ParseTestData
import subprocess
from nose.plugins.attrib import attr

test_data = ParseTestData()
ids = test_data.get_blueprints_ids()
#args = test_data.get_install_args()
#args_uninstall = test_data.get_args_uninstall()
args_upload = test_data.get_upload_args()

@attr(type="upload")
class UploadBlueprints:
    def upload_bp(self, arg):
        proc_upload = subprocess.run(arg)
        assert proc_upload.returncode == 0

    def test_uploads(self):
        for id in ids[:5]:
            yield self.upload_bp, args_upload.get(id)

@attr(type="install")
class InstallBlueprints:

    def install_bp(self, arg):
        pass

    def test_installs(self):
        pass



