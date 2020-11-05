from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError
import models as mds
from passlib.hash import pbkdf2_sha256


def invalid_credentials(form, field):
    """username and password checker"""
    username_entered = form.username.data
    password_entered = field.data

    user_object = mds.User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password incorrect")
    elif password_entered != user_object.password:
        raise ValidationError("Username or password incorrectg")


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField('username_label', validators=[InputRequired(message="Username Required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password Required"), invalid_credentials])
    submit_button = SubmitField('Login')


