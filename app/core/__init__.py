from flask import Blueprint

main = Blueprint('core', __name__)

from . import end_points
