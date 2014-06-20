from os import path
import yaml

CURRENT_DIR = path.dirname(path.realpath(__file__))
CONFIG_FILE = path.join(CURRENT_DIR, '..', '..', 'config', 'manager_config.yml')

config = None

def get_config():
    if config:
        return config
    else:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f)
    return config
