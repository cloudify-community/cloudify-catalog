import os
import json
import yaml
import logging
from catalog import check_bp_changed, get_changed_bps_path

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

class ParseTestData():

    def __init__(self, bps_scope='changed', catalog_path="./catalog.yaml", install_path= "./catalog_install.json", verbose = False):
        with open(catalog_path, "rb") as file_:
            self._yaml_data = yaml.load(file_, Loader=yaml.FullLoader)
        with open(install_path, "rb") as file_:
            self._json_data = json.load(file_)
        if(verbose):
            logging.info("YAML: {}".format(self._yaml_data))
            logging.info("JSON: {}".format(self._json_data))
        self._changed_bps_only = bps_scope =='changed'

    def get_tabs(self):
        tabs = [ item['name'] for item in self._yaml_data['topics'] ]
        return tabs

    def _get_bps(self):

        bps = [ item['blueprints'] for item in self._yaml_data['topics'] ]
        bps = [ item for itemw in bps for item in itemw ]
        if self._changed_bps_only:
            bps = [ bp for bp in self._filter_bps(bps) ] 
        return bps
    
    def _filter_bps(self, bps):
        changed_files = get_changed_bps_path()
        for bp in bps: 
            if check_bp_changed( bp['path'], changed_files):
                yield bp

    def get_create_deployment_args(self):

        args = {}

        for item in self._json_data:
            command = ["cfy", "deployments", "create", "-b", item.get("id") ]
            if item.get('inputs'):
                inputs = []
                for input, value in item.get('inputs').items():
                    inputs.append('-i {}={}'.format(input, value))
                command = command + inputs
            if item.get('parent'):
                command = command + [ '--labels csys-obj-parent:{}'.format(item.get('parent')) ]
            args[item.get('id')] = command
        return args

    def get_executions_start_args(self):
        args = {}
        for item in self._json_data:
            path = os.path.join
            command = [ "cfy", "executions", "start", "install", "-d", item.get("id") ]
            args[item.get('id')] = command
        return args

    def get_uninstall_args(self):
        args = {}
        for item in self._json_data:
            command = [ "cfy", "uninstall", "-f", item.get("id") ]
            args[item.get('id')] =  command
        return args

    def get_upload_args(self, from_build_cat = True):
        bps = self._get_bps()
        args = {}
        for blueprint in bps:
            blueprint_file = "blueprint.yaml"
            if "main_blueprint" in blueprint.keys():
                blueprint_file = blueprint.get("main_blueprint")
            if from_build_cat:
                path = os.path.join(['build', blueprint.get("id"), ".zip"])
                command = [ "cfy", "blueprints", "upload", "-b", path ]
            else:
                command = ["cfy", "blueprints", "upload", "-b", blueprint.get("id"), blueprint.get("path") + "/" + blueprint_file]
            args[ blueprint.get("id") ] = command
        return args

    def get_blueprints_ids(self):
        bps = self._get_bps()
        ids = []
        for blueprint in bps:
            print(blueprint)
            ids.append(blueprint.get("id"))
        return list(set(ids))

def main():

    tests = ParseTestData(True)
    bps = tests.get_upload_args()
    logging.info(bps)

if __name__ =="__main__":
    main() 