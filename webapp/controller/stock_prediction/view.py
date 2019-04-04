from . import stock_prediction
from flask import render_template, request, redirect, url_for, abort
from webapp.models import Stock_Basic
from library.datetime_function import date_validation


@stock_prediction.route('comprehensive_analysis', methods=['GET'])
def comprehensive_analysis():
    code = request.args.get('code')
    date = request.args.get('date')
    if code is None:
        return redirect(url_for('stock_prediction.comprehensive_analysis', code='000001.SZ'))
    else:
        result = Stock_Basic.query.filter_by(ts_code=code).first()
        if result is None:
            abort(404)
        else:
            date_validated, date_list = date_validation(date)
            stock = {'ts_code': result.ts_code, 'name': result.name, 'symbol': result.symbol}
            return render_template('stock_prediction/comprehensive_analysis.html', stock=stock, date=date_validated,
                                   date_list=date_list)

@stock_prediction.route('trend_prediction', methods=['GET'])
def trend_prediction():
    code = request.args.get('code')
    date = request.args.get('date')
    if code is None:
        return redirect(url_for('stock_prediction.trend_prediction', code='000001.SZ'))
    else:
        result = Stock_Basic.query.filter_by(ts_code=code).first()
        if result is None:
            abort(404)
        else:
            date_validated, date_list = date_validation(date)
            stock = {'ts_code': result.ts_code, 'name': result.name, 'symbol': result.symbol}
            return render_template('stock_prediction/trend_prediction.html', stock=stock, date=date_validated,
                                   date_list=date_list)

###############################################################

@stock_prediction.route('qjzn',methods=['GET','POST'])
def main_qjzn():
    code=request.args.get('code')
    if code is None:
        code='000001.SZ'
    return render_template('stock_prediction/qjzn.html',code = code,stock=None)


@stock_prediction.route('zycwzb',methods=['GET'])
def zycwzb():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/main_financial_indicators.html',stock=code)

@stock_prediction.route('zycwzb_year',methods=['GET'])
def zycwzb_year():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/main_financial_indicators_year.html',stock=code)

@stock_prediction.route('ylnl',methods=['GET'])
def ylnl():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/profit_ability.html',stock=code)

@stock_prediction.route('chnl',methods=['GET'])
def chnl():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/repaying_ability.html',stock=code)

@stock_prediction.route('cznl',methods=['GET'])
def cznl():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/growth_ability.html',stock=code)

@stock_prediction.route('yynl',methods=['GET'])
def yynl():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/operation_ability.html',stock=code)

@stock_prediction.route('lrbzy',methods=['GET'])
def lrbzy():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/profit_statement.html',stock=code)

@stock_prediction.route('lrbzy_year',methods=['GET'])
def lrbzy_year():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/profit_statement_year.html',stock=code)

@stock_prediction.route('zcfzbzy',methods=['GET'])
def zcfzbzy():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/balance_sheet.html',stock=code)

@stock_prediction.route('zcfzbzy_year',methods=['GET'])
def zcfzbzy_year():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/balance_sheet_year.html',stock=code)

@stock_prediction.route('xjjlbzy',methods=['GET'])
def xjjlbzy():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/cash_flow_statement.html',stock=code)

@stock_prediction.route('xjjlbzy_year',methods=['GET'])
def xjjlbzy_year():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/cash_flow_statement_year.html',stock=code)

@stock_prediction.route('cwbg',methods=['GET'])
def cwbg():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/report_aggregative_indicator.html',stock=code)

@stock_prediction.route('cwbg_lrb',methods=['GET'])
def cwbg_lrb():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/report_profit_statement.html',stock=code)

@stock_prediction.route('cwbg_xjllb',methods=['GET'])
def cwbg_xjllb():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/report_cash_flow_statement.html',stock=code)

@stock_prediction.route('cwbg_zcfzb',methods=['GET'])
def cwbg_zcfzb():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/report_balance.html',stock=code)

@stock_prediction.route('cwbg_year',methods=['GET'])
def cwbg_year():
    code = request.args.get('code')
    return render_template('stock_prediction/Financial_Index/report_aggregative_indicator_year.html',stock=code)


