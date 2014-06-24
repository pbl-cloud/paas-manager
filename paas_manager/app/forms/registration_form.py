from wtforms import Form, TextField, PasswordField, validators


class RegistrationForm(Form):
    email = TextField('email', [validators.Length(min=6)])
    password = PasswordField('password', [validators.Length(min=4)])
