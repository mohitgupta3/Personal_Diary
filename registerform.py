from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='This is a required field')])
    password = PasswordField('Password', [DataRequired(message='This is a required field'),
                                                EqualTo('confirm', message='Passwords mismatch detected')])
    confirm = PasswordField('Re-enter password', validators=[DataRequired(message='This is a required field')])
    submit = SubmitField('Complete registration')
