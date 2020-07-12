from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    review = TextAreaField('Pitch review')
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    name = StringField('Pitch title', validators=[DataRequired()])
    description = TextAreaField('Pitch description', validators=[DataRequired()])
    submit = SubmitField('Submit')
