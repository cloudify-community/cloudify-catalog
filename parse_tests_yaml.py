import json
import yaml
import logging

class ParseTestData():

    def __init__(self, catalog_path="./catalog.yaml", install_path= "./catalog_install.json", verbose = False):
        with open(catalog_path, "rb") as file_:
            self._yaml_data = yaml.load(file_, Loader=yaml.FullLoader)
        with open(install_path, "rb") as file_:
            self._json_data = json.load(file_)
        if(verbose): 
            logging.info("YAML: {}".format(self._yaml_data))
            logging.info("JSON: {}".format(self._json_data))

    def get_tabs(self):
        tabs = [ item['name'] for item in self._yaml_data['topics'] ]
        return tabs

    def _get_bps(self):
        bps = [ item['blueprints'] for item in self._yaml_data['topics'] ]
        bps = [ item for itemw in bps for item in itemw ]  
        return bps

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
            command = [ "cfy", "executions", "start", "install", "-d", item.get("id") ]
            args[item.get('id')] = command
        return args

    def get_uninstall_args(self):
        args = {}
        for item in self._json_data: 
            command = [ "cfy", "uninstall", "-f", item.get("id") ]
            args[item.get('id')] =  command
        return args

    def get_upload_args(self):
        bps = self._get_bps()
        args = {}
        for blueprint in bps:
            command = ["cfy", "blueprints", "upload", "-b", blueprint.get("id"), blueprint.get("path")+"/blueprint.yaml" ]
            args[ blueprint.get("id") ] = command
        return args
    
    def get_blueprints_ids(self):
        bps = self._get_bps()
        ids = []
        for blueprint in bps:
            ids.append(blueprint.get("id"))
        return list(set(ids))

if __name__ =="__main__":

    tests = ParseTestData()
    #print(tests.get_blueprints_ids())
    #print(tests.get_upload_args())
    print(tests.get_create_deployment_args())

