from parse_tests_yaml import ParseTestData
import subprocess
from nose.plugins.attrib import attr

test_data = ParseTestData()
ids = test_data.get_blueprints_ids()
#args = test_data.get_install_args()
#args_uninstall = test_data.get_args_uninstall()
args_upload = test_data.get_upload_args()


def upload_bp(arg):
    proc_upload = subprocess.run(arg)
    assert proc_upload.returncode == 0

@attr(type="upload")
def test_uploads():
    for id in ids[:2]:
        yield upload_bp, args_upload.get(id)


def install_bp(arg):
    pass

@attr(type="install")
def test_installs():
    pass