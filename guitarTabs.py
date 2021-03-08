from flask import Flask, render_template, url_for, request, send_file
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import click

from app.libs.constants import FILE_TYPES, OUTPUT_MIMES
from app.libs.form import SubmitForm
from app.libs.image import draw_picture
from app.libs.parsing import Parser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


bootstrap = Bootstrap(app)
moment = Moment(app)
parser = Parser()


@app.route("/export/<file_type>")
def export(file_type):
    FILE_TYPES[file_type](file_obj=open("static/pics/tabs.svg"),
                          write_to="static/pics/tabs.{}".format(file_type.lower()))
    return send_file("static/pics/tabs.{}".format(file_type.lower()), mimetype=OUTPUT_MIMES[file_type],
                     as_attachment=True, attachment_filename="tabs.{}".format(file_type.lower()))


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = SubmitForm()
    user_image = url_for('static', filename='pics/blank.svg')
    if form.is_submitted():
        form.validate()
        text = form.text.data
        result = parser.parse(text).data
        result = parser.transform(result)
        if result.success:
            draw_picture(result.data, form.title.data, form.bars.data)
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
