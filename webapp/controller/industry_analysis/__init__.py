from flask import Blueprint

industry_analysis = Blueprint('industry_analysis', __name__, url_prefix='/industry_analysis/')
from . import view, api
