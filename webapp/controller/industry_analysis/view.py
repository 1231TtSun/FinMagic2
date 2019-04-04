from . import industry_analysis
from flask import render_template

@industry_analysis.route('panorama_capital_flow',methods=['GET'])
def panorama_capital_flow():
    return render_template('industry_analysis/dynamic_panorama_the_venue/panorama_capital_flow.html')

@industry_analysis.route('panorama_active_trading',methods=['GET'])
def panorama_active_trading():
    return render_template('industry_analysis/dynamic_panorama_the_venue/panorama_active_trading.html')

@industry_analysis.route('panorama_trend_changes',methods=['GET'])
def panorama_trend_changes():
    return render_template('industry_analysis/dynamic_panorama_the_venue/panorama_trend_changes.html')

@industry_analysis.route('panorama_market_value_distribution',methods=['GET'])
def panorama_market_value_distribution():
    return render_template('industry_analysis/dynamic_panorama_the_venue/panorama_market_value_distribution.html')

@industry_analysis.route('panorama_dynamic_valuation',methods=['GET'])
def panorama_dynamic_valuation():
    return render_template('industry_analysis/dynamic_panorama_the_venue/panorama_dynamic_valuation.html')

@industry_analysis.route('click_heat_panorama',methods=['GET'])
def click_heat_panorama():
    return render_template('industry_analysis/offsite_dynamic_panorama/click_heat_panorama.html')

@industry_analysis.route('panorama_stock_bar_popularity',methods=['GET'])
def panorama_stock_bar_popularity():
    return render_template('industry_analysis/offsite_dynamic_panorama/panorama_stock_bar_popularity.html')

@industry_analysis.route('comparison_financial_indicators',methods=['GET'])
def comparison_financial_indicators():
    return render_template('industry_analysis/comparison_financial_indicators.html')

@industry_analysis.route('market_data_comparison',methods=['GET'])
def market_data_comparison():
    return render_template('industry_analysis/market_data_comparison.html')