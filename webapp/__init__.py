from flask import Flask
from .config import config
from .extensions import login_manager, csrf_protect
from .models import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    csrf_protect.init_app(app)
    db.init_app(app)

    # 模块注册
    from .controller.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .controller.administrator import administrator as administrator_blueprint
    app.register_blueprint(administrator_blueprint)
    from .controller.stock_prediction import stock_prediction as stock_prediction_blueprint
    app.register_blueprint(stock_prediction_blueprint)
    from .controller.index_prediction import index_prediction as index_prediction_blueprint
    app.register_blueprint(index_prediction_blueprint)
    from .controller.basal_data import basal_data as basal_data_blueprint
    app.register_blueprint(basal_data_blueprint)
    from .controller.industry_analysis import industry_analysis as industry_analysis_blueprint
    app.register_blueprint(industry_analysis_blueprint)
    from .controller.stock_recommendation import stock_recommendation as stock_recommendation_blueprint
    app.register_blueprint(stock_recommendation_blueprint)
    from .controller.additional_pages import additional_pages as additional_pages_blueprint
    app.register_blueprint(additional_pages_blueprint)

    return app
