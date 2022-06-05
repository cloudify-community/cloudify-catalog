import json

class ParseTestData():

    @staticmethod
    def load_data(file_path="./test-blueprints.json"):

        with open(file_path, "rb") as file_:
            return json.load(file_)


if __name__ == "__main__":
    
    data = ParseTestData.load_data()
    print(data)