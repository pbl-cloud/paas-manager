from . import app
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.datastructures import CombinedMultiDict
import os

from .models import Jobs, Users
from .forms import RegistrationForm, JobCreationForm
from .auth import current_user, user_signed_in
from . import queue_manager


def needs_authentication(fn):
    def wrapped(*args, **kwargs):
        if user_signed_in():
            return fn(*args, **kwargs)
        else:
            flash('ログインしてください。', 'danger')
            return redirect(url_for('index'))
    return wrapped


@app.route("/")
def index(job_form=None):
    if job_form is None:
        job_form = JobCreationForm(request.form)
    jobs = []
    if user_signed_in():
        options = {'order': 'id desc'}
        jobs = Jobs.query(user_id=current_user().id, _options=options)
    return render_template("index.html", jobs=jobs, job_form=job_form)


@app.route("/jobs/<int:job_id>")
def show_job(job_id):
    job = Jobs.find(job_id)
    if not job:
        # FIXME: use 404 properly
        flash("ジョブが見つかりませんでした。", 'danger')
        return redirect(url_for('index'))
    return render_template("job.html", job=job)


@app.route('/upload', methods=['POST'])
@needs_authentication
def upload():
    job_form = JobCreationForm()
    if request.method == 'POST' and job_form.validate_on_submit():
        args = request.form['arguments']
        job = Jobs.submit(current_user().id, request.files['jar_file'], args)
        queue_manager.enqueue_job(job)
        #gmail(file.filename, email)
        flash('ジョブが提出されました。', 'success')
        return redirect(url_for('index'))
    return index(job_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = Users.create(**form.data)
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
