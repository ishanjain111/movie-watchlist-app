from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class MovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    year = IntegerField("Year", validators=[InputRequired(), NumberRange(min=1800, message="Please enter year in format YYYY.")])
    submit = SubmitField("Add Movie")