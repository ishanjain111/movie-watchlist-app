from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo

class MovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    year = IntegerField("Year", validators=[InputRequired(), NumberRange(min=1800, message="Please enter year in format YYYY.")])
    submit = SubmitField("Add Movie")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                min=4,
                max=20,
                message="Your password must be between 4 and 20 characters long.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators= [ 
            InputRequired(),
            EqualTo(
                "password",
                message="This password did not match the one in the Password field.",
            )
        ]      
    )
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")