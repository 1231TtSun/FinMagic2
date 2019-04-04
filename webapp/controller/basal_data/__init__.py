from flask import Blueprint

basal_data = Blueprint('basal_data', __name__, url_prefix='/basal_data/')
from . import view, api
