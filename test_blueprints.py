from parse_tests import ParseTestData
import subprocess
import pytest

test_data = ParseTestData() 
ids = test_data.get_ids()
args = test_data.get_args()

@pytest.mark.parametrize('blueprint', ids, ids=ids)
def test_blueprints(blueprint):
    proc = subprocess.run(args.get(blueprint))
    assert proc.returncode == 0
   