from flask import Blueprint

administrator = Blueprint('administrator', __name__, url_prefix='/administrator/')
from . import view, api
