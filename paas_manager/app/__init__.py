from flask import Flask
from os import mkdir
from os.path import expanduser, exists
import sys
from kazoo.handlers.threading import TimeoutError
import signal

from ..settings import config
from .util import StreamConsumingMiddleware
from ..queue_manager import Manager

UPLOAD_FOLDER = expanduser(config['app']['upload_folder'])

if not exists(UPLOAD_FOLDER):
    mkdir(UPLOAD_FOLDER)

queue_manager = None

try:
    queue_manager = Manager()
except TimeoutError:
    print("Could not connect to ZooKeeper.", file=sys.stderr)
    sys.exit(1)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = config['security']['secret']
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)


def sigint_handler(signal, frame):
    print("Cleaning up...")
    queue_manager._terminated = True
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


from . import context_processors
from . import views
