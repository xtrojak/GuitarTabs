from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import click

from app.libs.form import SubmitForm
from app.libs.image import draw_picture
from app.libs.parsing import Parser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)
parser = Parser()


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = SubmitForm()
    user_image = url_for('static', filename='pics/blank.svg')
    if form.validate_on_submit():
        text = form.text.data
        result = parser.parse(text).data
        result = parser.transform(result)
        if result.success:
            draw_picture(result.data)
            user_image = url_for('static', filename='pics/tabs.svg')
    return render_template('index.html', form=form, name=name, user_image=user_image)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names != ('', ):
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
