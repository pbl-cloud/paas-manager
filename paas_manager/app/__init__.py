from flask import Flask
from os import mkdir
from os.path import expanduser, exists
from ..settings import config


UPLOAD_FOLDER = expanduser(config['app']['upload_folder'])

if not exists(UPLOAD_FOLDER):
    mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = config['security']['secret']

from . import context_processors
from . import views
