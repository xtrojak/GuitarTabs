import json
import os

from flask import render_template, url_for, request, send_file, redirect, session, Blueprint
from wtforms import ValidationError

from app.libs.constants import FILE_TYPES, OUTPUT_MIMES
from app.libs.image import draw_picture
from app.libs.parsing import parser, validate_syntax

from . import main
from .. import info_template


@main.route("/parse", methods=['POST'])
def parse():
    data = request.get_json()
    expression = data['expression']

    result = parser.parse(expression)
    response = {"success": result.success}

    if not result.success:
        response.update(result.data)
        response["expected"] = list(response["expected"])

    # test length

    return json.dumps(response)


@main.route("/export/<file_type>")
def export(file_type):
    from main import PATH
    source_file = os.path.join(PATH, 'static', 'pics', 'tabs.svg')
    target_file = os.path.join(PATH, 'static', 'pics', 'tabs.{}'.format(file_type.lower()))
    FILE_TYPES[file_type](file_obj=open(source_file),
                          write_to=target_file)
    return send_file("static/pics/tabs.{}".format(file_type.lower()), mimetype=OUTPUT_MIMES[file_type],
                     as_attachment=True, attachment_filename="tabs.{}".format(file_type.lower()))


@main.route('/compile', methods=['POST'])
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
            from main import PATH
            path = os.path.join(PATH, 'static', 'pics', 'tabs.svg')
            draw_picture(result.data, title, use_bars, path)
            session['user_image'] = url_for('static', filename='pics/tabs.svg')
    except ValidationError as e:
        print(e)

    return redirect(url_for('core.index'))


@main.route('/', methods=['GET'])
def index():
    user_image = session.get('user_image', url_for('static', filename='pics/blank.svg'))
    area_content = session.get('area_content', '')
    title = session.get('title', '')
    checked = session.get('checked', '')
    return render_template('index.html', user_image=user_image, area_content=area_content,
                           title=title, checked=checked, info=info_template)
