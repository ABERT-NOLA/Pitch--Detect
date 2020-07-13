from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from app import db
from app.models import Category


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    review = TextAreaField('Pitch review')
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    name = StringField('Pitch title', validators=[DataRequired()])
    description = TextAreaField('Pitch description', validators=[DataRequired()])
    category = QuerySelectField(label='Category',
                                query_factory=lambda: db.session.query(Category).all(),
                                get_pk=lambda item: item.id,
                                get_label=lambda item: item.name,
                                allow_blank=False)
    submit = SubmitField('Submit')


class VoteForm(FlaskForm):
    type = HiddenField('Vote', validators=[DataRequired()])


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
