#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug import secure_filename
from gmail import *
from hadoop_modules import HadoopModules
 
app = Flask(__name__)

UPLOAD_FOLDER = '/home/ubuntu/jar'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jar'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Item:
    def __init__(item, name, filename, status):
        item.name = name
        item.filename = filename
        item.status = status

class QueueManager:
    def __init__(self, jar_path, args):
        self.hadoop_modules = HadoopModules()
        self.jar_path = jar_path
        self.args = args
        self.result = ''
        self.resulterr = ''

    def piyo(self):

        def callback(stdout, stderr):
            self.result = stdout
            self.resulterr = stderr

        t = self.hm.start_hadoop(self.jar_path, self.args, callback)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS 

items = []

@app.route("/")
def index():
    return render_template("index.html", items=items)
	
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        file = request.files['jarfile']
        email = request.form['email']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            items.append( Item(request.form['username'], file.filename, 'waiting') )
            #gmail(file.filename, email)
	
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ログイン処理
    if request.method == 'POST' and _is_account_valid():
            # セッションにユーザ名を保存してからインデックスページにリダイレクトする
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    # ログインページを表示する
    return render_template('login.html')


# 正規のアカウントかチェックする関数
def _is_account_valid():
    # リクエストに username が含まれていれば通す
    if request.form.get('username') is None:
        return False
    return True


@app.route('/logout', methods=['GET'])
def logout():
    #セッションからユーザ名を取り除く (ログアウトの状態にする)
    session.pop('username', None)
    # ログインページにリダイレクトする
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)
