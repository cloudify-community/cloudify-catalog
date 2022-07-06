from xml.dom.xmlbuilder import _DOMInputSourceStringDataType
import yaml

class ParseTestData():

    def __init__(self, file_path="./catalog.yaml", verbose = False):
        with open(file_path, "rb") as file_:
            self._yaml_data = yaml.load(file_, Loader=yaml.FullLoader)
        if(verbose): 
            print(self._yaml_data)

    def get_tabs(self):
        tabs = [ item['name'] for item in self._yaml_data['topics'] ]
        return tabs

    def _get_bps(self):
        bps = [ item['blueprints'] for item in self._yaml_data['topics'] ]
        bps = [ item for itemw in bps for item in itemw]  
        return bps  
    
    def get_install_args(self):
        pass

    def get_uninstall_args(self):
        pass

    def get_upload_args(self):
        bps = self._get_bps()
        args = {}
        for blueprint in bps:
            command = ["cfy", "blueprints", "upload", "-b", blueprint.get("id"), blueprint.get("path")+"/blueprint.yaml" ]
            args[blueprint.get("id")] = command
        return args
    
    def get_blueprints_ids(self):
        bps = self._get_bps()
        ids = []
        for blueprint in bps:
            ids.append(blueprint.get("id"))
        return ids

if __name__ =="__main__":

    tests = ParseTestData()
    print(tests.get_blueprints_ids())
    print(tests.get_blueprints_args())

