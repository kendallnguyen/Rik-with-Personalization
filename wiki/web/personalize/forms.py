from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import InputRequired


class preferences(FlaskForm):
    method = RadioField('I want to: (must choose one)', choices=[('put', 'change all of my preferences'), ('patch', 'change some preferences'), ('post', 'create a new user')])
    name = StringField('Name', [InputRequired()])
    backgroundColor = StringField('BackgroundColor', [InputRequired()])
    textColor = StringField('TextColor', [InputRequired()])
    buttonColor = StringField('ButtonColor', [InputRequired()])
    font = StringField('Font', [InputRequired()])
    submit = SubmitField()
    delete = SubmitField('Yes, Delete Me')
    put = SubmitField('change all of my preferences')
    post = SubmitField('change some of my preferences')


