import json

class Utility:
    @staticmethod
    def read_json(config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
        