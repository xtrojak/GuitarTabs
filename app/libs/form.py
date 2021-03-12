from flask_wtf import FlaskForm
import wtforms

from app.libs.parsing import Parser

parser = Parser()


def validate_length(form, field):
    result = parser.parse(field.data)
    if not result.success:
        raise wtforms.ValidationError(result.data)
    result = parser.check_size(result.data)
    if not result.success:
        raise wtforms.ValidationError(result.data)


class SubmitForm(FlaskForm):
    text = wtforms.TextAreaField(label="", validators=[wtforms.validators.DataRequired(), validate_length])
    submit_button = wtforms.SubmitField(label="COMPILE")
    title = wtforms.StringField(label="Title:")
    bars = wtforms.BooleanField(label="Draw bars numbers")
