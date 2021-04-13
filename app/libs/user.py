from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from wtforms import StringField, PasswordField, validators, SubmitField
import uuid
from flask_login import UserMixin

from app import db, login_manager


class UserNotFoundException(Exception):
    pass


class UserManager:
    def __init__(self):
        self.anonymous_users = set()

    @staticmethod
    def register_user(user):
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def get_user(email):
        return User.get_by_email(email)

    def register_anonymous_user(self, userid):
        self.anonymous_users.add(userid)

    def load_anonymous_user(self, userid):
        if userid in self.anonymous_users:
            return MyAnonymousUser(userid)
        else:
            raise UserNotFoundException


class User(UserMixin, db.Model):
    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    @staticmethod
    def get_by_id(userid):
        result = User.query.filter_by(id=userid).first()
        if result:
            return result
        else:
            raise UserNotFoundException

    @staticmethod
    def get_by_email(email):
        result = User.query.filter_by(email=email).first()
        if result:
            return result
        else:
            raise UserNotFoundException


class MyAnonymousUser:
    def __init__(self, id=None):
        self.id = str(uuid.uuid4()) if id is None else id

    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get_by_id(userid)
    except UserNotFoundException:
        return None


# Creating Registration Form contains username, name, email, password and confirm password.
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])
    submit = SubmitField('Register')


user_manager = UserManager()

