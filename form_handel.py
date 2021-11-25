from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields.core import DateField, StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
    name = StringField("What should we call you?", validators=[
                       DataRequired(message="We can't call you '', It's inappropriate.")])
    email = StringField("Your Email", validators=[DataRequired(
        "Please provide an email address"), Email("Email format is incorrect.")])
    password = PasswordField("A Strong Password", validators=[
                             DataRequired("Password is required")])
    submit = SubmitField("Sign Me Up")
