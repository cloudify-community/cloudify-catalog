import json

class ParseTestData():

    def __init__(self, file_path="./test-blueprints.json"):
        with open(file_path, "rb") as file_:
            self._json_data = json.load(file_)

    def get_ids(self):
        return [ item.get("name") for item in self._json_data ]

    def get_args(self):
        args = {}
        for blueprint in self._json_data:
            command = [ "cfy","install","-b", blueprint.get("name"), blueprint.get("path")+"/blueprint.yaml" ]
            args_inputs = []
            if blueprint.get("inputs"):        
                for k, v in blueprint.get('inputs').items():
                    args_inputs.append("-i")
                    args_inputs.append("=".join([k, v]))
            args[blueprint.get("name")] = command+args_inputs
        return args

    def get_args_uninstall(self):
        args = {}
        for blueprint in self._json_data:
            command = ["cfy", "exec", "start", "uninstall", "--force", "-d", blueprint.get("name") ,"-p", "ignore_failure=True"]
            args[blueprint.get("name")] = command
        return args
    
    def get_args_upload(self):
        args = {}
        for blueprint in self._json_data:
            command = ["cfy", "blueprints", "upload", "-b", blueprint.get("name"), blueprint.get("path")+"/blueprint.yaml" ]
            args[blueprint.get("name")] = command
        return args


    
if __name__ == "__main__":
    
    data = ParseTestData()
    print(data.get_ids())
    print(data.get_args())