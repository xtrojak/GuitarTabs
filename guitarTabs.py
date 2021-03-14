from flask import Flask, render_template, url_for, request, send_file, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from wtforms import ValidationError
import click

from app.libs.constants import FILE_TYPES, OUTPUT_MIMES
from app.libs.image import draw_picture
from app.libs.parsing import parser, validate_syntax

CODEMIRROR_LANGUAGES = ['python', 'html']
WTF_CSRF_ENABLED = True
SECRET_KEY = 'hard to guess string'
SEND_FILE_MAX_AGE_DEFAULT = 0

app = Flask(__name__)
app.config.from_object(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/info")
def info():
    # TBD
    return redirect(url_for('index'))


@app.route("/export/<file_type>")
def export(file_type):
    FILE_TYPES[file_type](file_obj=open("static/pics/tabs.svg"),
                          write_to="static/pics/tabs.{}".format(file_type.lower()))
    return send_file("static/pics/tabs.{}".format(file_type.lower()), mimetype=OUTPUT_MIMES[file_type],
                     as_attachment=True, attachment_filename="tabs.{}".format(file_type.lower()))


@app.route('/compile', methods=['POST'])
def compile():
    text = request.form['code_area']
    session['area_content'] = text
    try:
        # raises exception if not OK
        data = validate_syntax(text)
        result = parser.transform(data)

        use_bars = True if 'bars' in request.form else False
        session['checked'] = 'checked' if use_bars else ''
        title = request.form['title']
        session['title'] = title

        if result.success:
            draw_picture(result.data, title, use_bars)
            session['user_image'] = url_for('static', filename='pics/tabs.svg')
    except ValidationError as e:
        print(e)

    return redirect(url_for('index'))


@app.route('/', methods=['GET'])
def index():
    user_image = session.get('user_image', url_for('static', filename='pics/blank.svg'))
    area_content = session.get('area_content', '')
    title = session.get('title', '')
    checked = session.get('checked', '')
    return render_template('index.html', user_image=user_image, area_content=area_content,
                           title=title, checked=checked)


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
