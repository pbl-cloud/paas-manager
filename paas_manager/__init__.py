import logging
import os

from .settings import config
from paas_manager.app import app


root_logger = logging.getLogger()
log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
root_logger.setLevel(getattr(logging, config['logging']['level']))
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

requests_log = logging.getLogger("kazoo")
requests_log.setLevel(logging.WARNING)


if 'filename' in config['logging']:
    log_dir = os.path.dirname(config['logging']['filename'])
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    file_handler = logging.FileHandler(config['logging']['filename'])
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
