from . import app
from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename
import os

from .models import Jobs

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'])

jobs = Jobs()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    items = []
    return render_template("index.html", items=items)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # email = request.form['email']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            items.append( Item(request.form['username'], file.filename, 'waiting') )
            #gmail(file.filename, email)

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if _is_account_valid():
            # セッションにユーザ名を保存してからインデックスページにリダイレクトする
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html')


def _is_account_valid():
    if request.form.get('username') is None:
        return False
    return True


@app.route('/logout', methods=['GET'])
def logout():
    #セッションからユーザ名を取り除く (ログアウトの状態にする)
    session.pop('username', None)
    return redirect(url_for('index'))
