import json
import os
import flask_login
from flask import render_template, url_for, request, send_file, redirect, session, Blueprint, flash, \
    get_flashed_messages
from wtforms import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.constants import FILE_TYPES, OUTPUT_MIMES
from app.libs.image import draw_picture
from app.libs.parsing import parser, validate_syntax

from . import main
from .. import info_template
from ..libs.user import User, RegisterForm, load_user, UserNotFoundException, user_manager


@main.before_request
def register_session():
    if 'uid' not in session:
        session['uid'] = flask_login.current_user.get_id()
        if flask_login.current_user.is_anonymous:
            user_manager.register_anonymous_user(flask_login.current_user.get_id())
    else:
        if flask_login.current_user.is_anonymous:
            try:
                flask_login.current_user = user_manager.load_anonymous_user(session['uid'])
            except UserNotFoundException:
                user_manager.register_anonymous_user(session['uid'])
        else:
            flask_login.current_user = load_user(session['uid'])


@main.route('/register', methods=['POST'])
def register():
    hashed_password = generate_password_hash(request.form['password'], method='sha256')

    new_user = User(id=flask_login.current_user.get_id(),
                    email=request.form['email'],
                    password=hashed_password)

    success = user_manager.register_user(new_user)
    if success:
        flash('You have successfully registered.', 'success')
    else:
        flash('User exists, please login.', 'danger')
        session['show_login_on_page_load'] = True
    return redirect(url_for('core.index'))


@main.route('/login', methods=['POST'])
def login():
    try:
        user = user_manager.get_user(request.form['email'])
        if check_password_hash(user.password, request.form['password']):
            session['logged_in'] = True
            flash('Logged in successfully.', 'success')
            # After successful login, redirecting to home page
            return redirect(url_for('core.index'))
        else:
            # if password is in correct, redirect to login page
            flash('Password Incorrect', 'danger')
            session['show_login_on_page_load'] = True
            return redirect(url_for('core.index'))
    except UserNotFoundException:
        flash('Username Incorrect', 'danger')
        session['show_register_on_page_load'] = True
        return redirect(url_for('core.index'))


@main.route('/logout', methods=['POST'])
def logout():
    # Login and validate the user.
    # user should be an instance of your `User` class
    login_user(user)

    flash('Logged out successfully.', 'success')

    return redirect(url_for('core.index'))


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
    source_file = os.path.join(PATH, 'static', 'pics', 'tabs_{}.svg'.format(session['uid']))
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
            path = os.path.join(PATH, 'static', 'pics', 'tabs_{}.svg'.format(session['uid']))
            draw_picture(result.data, title, use_bars, path)
            session['user_image'] = url_for('static', filename='pics/tabs_{}.svg'.format(session['uid']))
    except ValidationError as e:
        print(e)

    return redirect(url_for('core.index'))


@main.route('/', methods=['GET'])
def index():
    user_image = session.get('user_image', url_for('static', filename='pics/blank.svg'))
    area_content = session.get('area_content', '')
    title = session.get('title', '')
    checked = session.get('checked', '')
    show_login_on_page_load = session.pop('show_login_on_page_load', False)
    show_register_on_page_load = session.pop('show_register_on_page_load', False)

    register_form = RegisterForm()

    print(get_flashed_messages())

    return render_template('index.html', user_image=user_image, area_content=area_content,
                           title=title, checked=checked, info=info_template, register=register_form,
                           show_login_on_page_load=show_login_on_page_load,
                           show_register_on_page_load=show_register_on_page_load)
