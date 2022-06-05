from parse_tests import ParseTestData
import subprocess
import pytest

blueprints = ParseTestData.load_data() 

@pytest.mark.parametrize('blueprint', blueprints)
def test_blueprints(blueprint):
    args = [ "cfy","install","-b", blueprint.get("name"), blueprint.get("path")+"/blueprint.yaml" ] 
    if blueprint.get("inputs"):
        args_inputs = []
        for k, v in blueprint.get('inputs').items():
            args_inputs.append("-i")
            args_inputs.append("=".join([k, v]))
        args = args+args_inputs
    proc = subprocess.run(args)
    assert proc.returncode == 0
   