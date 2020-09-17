from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class TemperatureForm(FlaskForm):
    temp = IntegerField("Temperature", validators = [DataRequired("You must enter an integer value")])
    section = SelectField("Section", choices = [('Outside', 'Outside'), ('Heating', 'Heating'), ('Planting', 'Planting')])
    submit = SubmitField('Record Temperature')