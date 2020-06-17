"""Flask Feedback Forms"""

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """Login form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8, max=20)],
    )

class RegistrationForm(FlaskForm):
    """Registration form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8, max=20)],
    )
    email = StringField(
        "E-mail",
        validators=[InputRequired(), Email(), Length(max=254)]
    )
    first_name = StringField(
        "First Name",
        validators[InputRequired(), Length(max=30)]
    )
    last_name = StringField(
        "Last Name",
        validators[InputRequired(), Length(max=30)]
    )

class FeedbackForm(FlaskForm):
    """Feedback form"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )