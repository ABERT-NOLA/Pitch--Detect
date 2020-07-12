from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    title = StringField('Review title', validators=[DataRequired()])

    review = TextAreaField('Pitch review')

    submit = SubmitField('Submit')
