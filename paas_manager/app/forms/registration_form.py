from wtforms import Form, TextField, PasswordField, validators
from ..models import Users


class RegistrationForm(Form):
    email = TextField('メールアドレス', [validators.Length(min=6)])
    password = PasswordField('パスワード', [validators.Length(min=4)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if Users.exists({'email': self.email.data}):
            self.email.errors.append('このメールアドレスが既に登録されています。')
            return False
        return True
