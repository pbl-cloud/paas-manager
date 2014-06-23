from os import path
import yaml

CURRENT_DIR = path.dirname(path.realpath(__file__))
CONFIG_DIR = path.join(CURRENT_DIR, '..', 'config')
CONFIG_FILE = path.join(CONFIG_DIR, 'paas_manager.yml')
LOCAL_CONFIG_FILE = path.join(CONFIG_DIR, 'paas_manager.local.yml')

def dict_merge(a, b):
    if not isinstance(b, dict):
        return b
    for k, v in b.items():
        if k in a and isinstance(a[k], dict):
                a[k] = dict_merge(a[k], v)
        else:
            a[k] = v
    return a


def get_config():
    with open(CONFIG_FILE, 'r') as f:
        conf = yaml.load(f)

    if path.exists(LOCAL_CONFIG_FILE):
        with open(LOCAL_CONFIG_FILE, 'r') as f:
            local_conf = yaml.load(f)

    return dict_merge(conf, local_conf)


config = get_config()
