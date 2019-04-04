from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/')
from . import view, api, error
