from parse_tests import ParseTestData
import subprocess
import pytest

test_data = ParseTestData() 
ids = test_data.get_ids()
args = test_data.get_args()
args_uninstall = test_data.get_args_uninstall()

@pytest.mark.parametrize('blueprint', ids, ids=ids)
def test_blueprints(blueprint):
    proc_install = subprocess.run(args.get(blueprint))
    subprocess.Popen(args_uninstall.get(blueprint))
    assert proc_install.returncode == 0
   