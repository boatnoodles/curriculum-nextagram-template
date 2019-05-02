from wtforms import Form, BooleanField, StringField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(
        min=4, max=25), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(
        min=6, max=35), validators.DataRequired()])
    password = StringField(
        'Password', [validators.Length(min=6), validators.DataRequired(), validators.EqualTo('confirm', message="Passwords must match")])
    confirm = StringField('Enter your password again to confirm')
    accept_rules = BooleanField('I accept the site rules', [
                                validators.InputRequired()])
