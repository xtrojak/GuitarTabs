from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import wtforms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class SubmitForm(FlaskForm):
    text = wtforms.TextAreaField(label="code area", validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField(label="Translate")


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = SubmitForm()
    user_image = url_for('static', filename='front.png')
    if form.validate_on_submit():
        text = form.text.data
        form.text.data = ''
        user_image = url_for('static', filename='pic.jpg')
    return render_template('index.html', form=form, name=name, user_image=user_image)
