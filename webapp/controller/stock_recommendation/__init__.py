from flask import Blueprint

stock_recommendation = Blueprint('stock_recommendation', __name__, url_prefix='/stock_recommendation/')
from . import view, api
