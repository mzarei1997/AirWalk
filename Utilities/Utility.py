import json

class Utility:
    @staticmethod
    def read_json(config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config

    @staticmethod
    def check_qos(incoming_qos: int):
        valid_qos = [0, 1, 2]
        if incoming_qos not in valid_qos:
            raise ValueError(f"Invalid QoS value: {incoming_qos}. Must be one of {valid_qos}.")
        