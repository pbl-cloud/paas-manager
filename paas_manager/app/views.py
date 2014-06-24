from . import app
from flask import render_template, request, redirect, url_for, session
from werkzeug import secure_filename
import os

from .models import Jobs, Users
from .forms import RegistrationForm

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'])

jobs = Jobs()
users = Users()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# TODO: move to other module
# TODO: cache result for current request
def current_user():
    if 'user_id' in session:
        return Users.find(session['user_id'])
    return None


def user_signed_in():
    return current_user() is not None


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
            items.append(
                Item(request.form['username'], file.filename, 'waiting'))
            #gmail(file.filename, email)

    return redirect(url_for('index'))


@app.route('/sign_up')
def signup():
    return render_template('sign_up.html')


@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users.create(form.data)
        session['user_id'] = user.id
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    user = users.authorize(request.form['email'], request.form['password'])
    if user:
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    #セッションからユーザ名を取り除く (ログアウトの状態にする)
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.context_processor
def inject_current_user():
    return {'current_user': current_user}


@app.context_processor
def inject_user_signed_in():
    return {'user_signed_in': user_signed_in}
