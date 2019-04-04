from flask import Blueprint

stock_prediction = Blueprint('stock_prediction', __name__, url_prefix='/stock_prediction/')
from . import view, api
