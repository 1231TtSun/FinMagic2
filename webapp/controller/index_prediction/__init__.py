from flask import Blueprint

index_prediction = Blueprint('index_prediction', __name__, url_prefix='/index_prediction/')
from . import view, api
