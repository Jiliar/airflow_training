import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, 'r') as file:
            self.config = json.load(file)

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def all(self):
        return self.config