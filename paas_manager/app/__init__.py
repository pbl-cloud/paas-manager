from flask import Flask
from os import mkdir
from os.path import expanduser, join, exists

UPLOAD_FOLDER = join(expanduser("~"), "jars")

if not exists(UPLOAD_FOLDER):
    mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from . import views
