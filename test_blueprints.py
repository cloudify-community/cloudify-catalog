from parameterized import parameterized
from parse_tests import ParseTestData
import subprocess
import unittest

test_data = ParseTestData()
ids = test_data.get_ids()
args = test_data.get_args()
args_uninstall = test_data.get_args_uninstall()


class TestBlueprint(unittest.TestCase):

    def test_blueprints(self):
        for blueprint in ids:
            with self.subTest(blueprint):
                proc_install = subprocess.run(args.get(blueprint))
                proc_uninstall = subprocess.run(
                    args_uninstall.get(blueprint), timeout=300)
                self.assertTrue(proc_install.returncode ==
                            0 and proc_uninstall.returncode == 0)

if __name__ == "__main__":
    unittest.main()