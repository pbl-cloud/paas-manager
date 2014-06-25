from . import app
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug import secure_filename
import os

from .models import Jobs, Users
from .forms import RegistrationForm
from .auth import current_user, user_signed_in

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def needs_authentication(fn):
    def wrapped(*args, **kwargs):
        if user_signed_in():
            return fn(*args, **kwargs)
        else:
            flash('ログインしてください。', 'danger')
            return redirect(url_for('index'))
    return wrapped


@app.route("/")
def index():
    items = []
    if user_signed_in():
        items = Jobs.query({'user_id': current_user().id})
    return render_template("index.html", items=items)


@app.route('/upload', methods=['POST'])
@needs_authentication
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # email = request.form['email']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Jobs.create({
                'user_id': current_user().id,
                'filename': file.filename
            })
            #gmail(file.filename, email)

    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users.create(form.data)
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST'])
def login():
    user = Users.authorize(request.form['email'], request.form['password'])
    if user:
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
