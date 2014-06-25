from wtforms import TextField, PasswordField, validators
from flask_wtf import Form
from ..models import Users


def too_short_msg(n):
    return "{0}文字以上入力してください。".format(n)


class RegistrationForm(Form):
    email = TextField('メールアドレス', [validators.Length(min=6, message=too_short_msg(6))])
    password = PasswordField('パスワード', [validators.Length(min=4, message=too_short_msg(4))])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if Users.exists(email=self.email.data):
            self.email.errors.append('このメールアドレスが既に登録されています。')
            return False
        return True
