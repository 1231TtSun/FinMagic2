from flask import Blueprint

additional_pages = Blueprint('additional_pages', __name__, url_prefix='/additional_pages/')
from . import view, api
