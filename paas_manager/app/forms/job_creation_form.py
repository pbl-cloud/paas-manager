from flask_wtf import Form
from wtforms import TextField
from flask_wtf.file import FileField, FileAllowed, FileRequired

NO_FILE_MSG = 'ファイルを指定してください。'
NOT_JAR_MSG = 'jarファイルを選択してください。'

file_validators = [
    FileRequired(message=NO_FILE_MSG),
    FileAllowed(['jar'], NOT_JAR_MSG)
]


class JobCreationForm(Form):
    jar_file = FileField('Hadoop MapReduce用のjar', validators=file_validators)
    arguments = TextField('引数')
