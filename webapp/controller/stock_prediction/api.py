from . import stock_prediction
from flask import request, jsonify
from webapp.models import *
from library.datetime_function import get_offset_date


@stock_prediction.route('api_comprehensive_analysis', methods=['GET'])
def api_comprehensive_analysis():
    code = request.args.get('code')
    date = request.args.get('date')
    bar_data = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == code, Stock_Daily_Bar.trade_date <= date,
                                            Stock_Daily_Bar.trade_date >= get_offset_date(date, -730)).order_by(
        Stock_Daily_Bar.trade_date.asc()).all()
    basic_data = Stock_Daily_Basic.query.filter_by(ts_code=code, trade_date=date).first()
    # 要判断上面两个查询结果非空
    today_bar_data = {'open': bar_data[-1].open, 'close': bar_data[-1].close, 'high': bar_data[-1].high,
                      'low': bar_data[-1].low, 'change': bar_data[-1].change, 'pct_chg': bar_data[-1].pct_chg,
                      'pre_close': bar_data[-1].pre_close, 'vol': bar_data[-1].vol, 'amount': bar_data[-1].amount}
    today_basic_data = {'turnover_rate': basic_data.turnover_rate, 'pe': basic_data.pe, 'pb': basic_data.pb,
                        'circ_mv': basic_data.circ_mv}
    short_trend_data = []
    k_line_data = []
    one_year_data = []
    for i in bar_data[-60:]:
        short_trend_data.append(i.close)
    for i in bar_data[-250:]:
        one_year_data.append(i.close)
    for i in bar_data:
        trade_date = i.trade_date
        k_line_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    one_year_min = min(one_year_data)
    one_year_max = max(one_year_data)
    concepts = []
    company_data = Stock_Company_Extend.query.join(Stock_Company,
                                                   Stock_Company_Extend.ts_code == Stock_Company.ts_code).add_columns(
        Stock_Company.province, Stock_Company.city).join(Stock_Industry_SW_3,
                                                         Stock_Company_Extend.industry_sw_code == Stock_Industry_SW_3.industry_sw_3_code).add_columns(
        Stock_Industry_SW_3.industry_sw_3_name).join(
        Stock_Industry_SW_2, Stock_Industry_SW_3.belong_to == Stock_Industry_SW_2.industry_sw_2_code).add_columns(
        Stock_Industry_SW_2.industry_sw_2_name).join(
        Stock_Industry_SW_1, Stock_Industry_SW_2.belong_to == Stock_Industry_SW_1.industry_sw_1_code).add_columns(
        Stock_Industry_SW_1.industry_sw_1_name).filter(
        Stock_Company_Extend.ts_code == code).first()
    industry = [company_data.industry_sw_1_name, company_data.industry_sw_2_name, company_data.industry_sw_3_name]
    area = [company_data.province, company_data.city]
    concept_data = Stock_Concept_Detail.query.join(Stock_Concept_List,
                                                   Stock_Concept_Detail.concept_code == Stock_Concept_List.concept_code).add_columns(
        Stock_Concept_List.concept_name).filter(Stock_Concept_Detail.ts_code == code,
                                                Stock_Concept_List.src == 'wind').all()
    for i in concept_data:
        concepts.append(i.concept_name)
    return jsonify(
        {'today_bar_data': today_bar_data, 'today_basic_data': today_basic_data, 'short_trend_data': short_trend_data,
         'k_line_data': k_line_data, 'one_year_data': {'min': one_year_min, 'max': one_year_max},
         'company_and_concept': {'area': area, 'industry': industry, 'concept': concepts}})


@stock_prediction.route('api_trend_prediction', methods=['GET'])
def api_trend_prediction():
    code = request.args.get('code')
    date = request.args.get('date')
    bar_data = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == code, Stock_Daily_Bar.trade_date <= date,
                                            Stock_Daily_Bar.trade_date >= get_offset_date(date, -120)).order_by(
        Stock_Daily_Bar.trade_date.asc()).all()
    basic_data = Stock_Daily_Basic.query.filter_by(ts_code=code, trade_date=date).first()
    today_bar_data = {'open': bar_data[-1].open, 'close': bar_data[-1].close, 'high': bar_data[-1].high,
                      'low': bar_data[-1].low, 'change': bar_data[-1].change, 'pct_chg': bar_data[-1].pct_chg,
                      'pre_close': bar_data[-1].pre_close, 'vol': bar_data[-1].vol, 'amount': bar_data[-1].amount}

    ####################################应对数据库不完全 临时措施
    if basic_data is None:
        today_basic_data = {'turnover_rate': 0, 'pe': 0, 'pb': 0,
                            'circ_mv': 0}
    else:
        today_basic_data = {'turnover_rate': basic_data.turnover_rate, 'pe': basic_data.pe, 'pb': basic_data.pb,
                            'circ_mv': basic_data.circ_mv}
    #################################正常应该修改

    trade_point_data = Model_Trading_Point.query.filter(Model_Trading_Point.ts_code == code,
                                                        Model_Trading_Point.trade_date <= date,
                                                        Model_Trading_Point.trade_date >= get_offset_date(date,
                                                                                                          -120)).order_by(
        Model_Trading_Point.trade_date.asc()).all()
    aggressive_requirement = '维持现状'
    steady_requirement = '维持现状'
    trade_point_line_data = []
    aggressive_trade_point = []
    steady_trade_point = []
    for i in bar_data:
        trade_date = i.trade_date
        trade_point_line_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    for i in trade_point_data:
        trade_date = i.trade_date
        if i.aggressive_buy_point is True:
            close = (Stock_Daily_Bar.query.filter_by(ts_code=code, trade_date=trade_date).first()).close
            aggressive_trade_point.append(
                [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), close, '买点'])
            if trade_date == date:
                aggressive_requirement = i.aggressive_buy_requirement
        if i.aggressive_sell_point is True:
            close = (Stock_Daily_Bar.query.filter_by(ts_code=code, trade_date=trade_date).first()).close
            aggressive_trade_point.append(
                [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), close, '卖点'])
            if trade_date == date:
                aggressive_requirement = i.aggressive_sell_requirement
        if i.steady_buy_point is True:
            close = (Stock_Daily_Bar.query.filter_by(ts_code=code, trade_date=trade_date).first()).close
            steady_trade_point.append([(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), close, '买点'])
            if trade_date == date:
                steady_requirement = i.steady_buy_requirement
        if i.steady_sell_point is True:
            close = (Stock_Daily_Bar.query.filter_by(ts_code=code, trade_date=trade_date).first()).close
            steady_trade_point.append([(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), close, '卖点'])
            if trade_date == date:
                steady_requirement = i.steady_sell_requirement
    trend_forecast_result = Model_Trend_Forecast.query.filter_by(ts_code=code, trade_date=date).first()
    first_vote = [trend_forecast_result.first_fall_vote, trend_forecast_result.first_maintain_vote,
                  trend_forecast_result.first_rise_vote]
    second_vote = [trend_forecast_result.second_fall_vote, trend_forecast_result.second_maintain_vote,
                   trend_forecast_result.second_rise_vote]
    third_vote = [trend_forecast_result.third_fall_vote, trend_forecast_result.third_maintain_vote,
                  trend_forecast_result.third_rise_vote]

    similarity_data = []
    similarity_1_data = []
    similarity_2_data = []
    similarity_3_data = []
    similarity_match_1_data = []
    similarity_match_2_data = []
    similarity_match_3_data = []
    mark_line = [
        (bar_data[-20].trade_date[0:4] + '/' + bar_data[-20].trade_date[4:6] + '/' + bar_data[-20].trade_date[6:8]),
        (bar_data[-1].trade_date[0:4] + '/' + bar_data[-1].trade_date[4:6] + '/' + bar_data[-1].trade_date[6:8])]
    similarity_short_term_result = Model_Similarity_Short_Term.query.filter_by(ts_code=code, trade_date=date).first()
    similarity_1_stock = Stock_Basic.query.filter_by(ts_code=similarity_short_term_result.similarity_1_code).first()
    similarity_2_stock = Stock_Basic.query.filter_by(ts_code=similarity_short_term_result.similarity_2_code).first()
    similarity_3_stock = Stock_Basic.query.filter_by(ts_code=similarity_short_term_result.similarity_3_code).first()
    similarity_1_result = Stock_Daily_Bar.query.filter(
        Stock_Daily_Bar.ts_code == similarity_short_term_result.similarity_1_code,
        Stock_Daily_Bar.trade_date <= similarity_short_term_result.similarity_1_prediction_end_time,).order_by(Stock_Daily_Bar.trade_date.desc()).limit(90).all()
    similarity_2_result = Stock_Daily_Bar.query.filter(
        Stock_Daily_Bar.ts_code == similarity_short_term_result.similarity_2_code,
        Stock_Daily_Bar.trade_date <= similarity_short_term_result.similarity_2_prediction_end_time,).order_by(Stock_Daily_Bar.trade_date.desc()).limit(90).all()
    similarity_3_result = Stock_Daily_Bar.query.filter(
        Stock_Daily_Bar.ts_code == similarity_short_term_result.similarity_3_code,
        Stock_Daily_Bar.trade_date <= similarity_short_term_result.similarity_3_prediction_end_time,).order_by(Stock_Daily_Bar.trade_date.desc()).limit(90).all()
    similarity_1_result.reverse()
    similarity_2_result.reverse()
    similarity_3_result.reverse()
    for i in bar_data[-60:]:
        trade_date = i.trade_date
        similarity_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    for i in similarity_1_result[-30:]:
        factor=bar_data[-1].close/similarity_1_result[-31].close
        trade_date = i.trade_date
        similarity_1_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open*factor, i.close*factor, i.low*factor, i.high*factor,
             i.amount])
    for i in similarity_2_result[-30:]:
        factor=bar_data[-1].close/similarity_2_result[-31].close
        trade_date = i.trade_date
        similarity_2_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open*factor, i.close*factor, i.low*factor, i.high*factor,
             i.amount])
    for i in similarity_3_result[-30:]:
        factor=bar_data[-1].close/similarity_3_result[-31].close
        trade_date = i.trade_date
        similarity_3_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open*factor, i.close*factor, i.low*factor, i.high*factor,
             i.amount])
    similarity_1_data=similarity_data+similarity_1_data
    similarity_2_data = similarity_data + similarity_2_data
    similarity_3_data = similarity_data + similarity_3_data
    for i in similarity_1_result:
        trade_date = i.trade_date
        similarity_match_1_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    for i in similarity_2_result:
        trade_date = i.trade_date
        similarity_match_2_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    for i in similarity_3_result:
        trade_date = i.trade_date
        similarity_match_3_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    similarity_match_mark_line_1 = [(similarity_short_term_result.similarity_1_matching_start_time[0:4] + '/' + similarity_short_term_result.similarity_1_matching_start_time[4:6] + '/' + similarity_short_term_result.similarity_1_matching_start_time[6:8]),
        (similarity_short_term_result.similarity_1_matching_end_time[0:4] + '/' + similarity_short_term_result.similarity_1_matching_end_time[4:6] + '/' + similarity_short_term_result.similarity_1_matching_end_time[6:8])]
    similarity_match_mark_line_2 = [(similarity_short_term_result.similarity_2_matching_start_time[0:4] + '/' + similarity_short_term_result.similarity_2_matching_start_time[4:6] + '/' + similarity_short_term_result.similarity_2_matching_start_time[6:8]),
        (similarity_short_term_result.similarity_2_matching_end_time[0:4] + '/' + similarity_short_term_result.similarity_2_matching_end_time[4:6] + '/' + similarity_short_term_result.similarity_2_matching_end_time[6:8])]
    similarity_match_mark_line_3 = [(similarity_short_term_result.similarity_3_matching_start_time[0:4] + '/' + similarity_short_term_result.similarity_3_matching_start_time[4:6] + '/' +similarity_short_term_result.similarity_3_matching_start_time[6:8]),
        (similarity_short_term_result.similarity_3_matching_end_time[0:4] + '/' + similarity_short_term_result.similarity_3_matching_end_time[4:6] + '/' + similarity_short_term_result.similarity_3_matching_end_time[6:8])]
    sparkline_data = []
    similarity_1_sparkline_data = []
    similarity_2_sparkline_data = []
    similarity_3_sparkline_data = []
    for i in bar_data[-20:]:
        sparkline_data.append(i.pct_chg)
    sparkline_data.extend([None]*30)
    for i in similarity_1_result[-50:]:
        similarity_1_sparkline_data.append(i.pct_chg)
    for i in similarity_2_result[-50:]:
        similarity_2_sparkline_data.append(i.pct_chg)
    for i in similarity_3_result[-50:]:
        similarity_3_sparkline_data.append(i.pct_chg)
    similarity_1_table_data = []
    similarity_2_table_data = []
    similarity_3_table_data = []
    for i in similarity_1_result[-30:]:
        similarity_1_table_data.append([i.pct_chg, i.open, i.close, i.high, i.low, i.vol])
    for i in similarity_2_result[-30:]:
        similarity_2_table_data.append([i.pct_chg, i.open, i.close, i.high, i.low, i.vol])
    for i in similarity_3_result[-30:]:
        similarity_3_table_data.append([i.pct_chg, i.open, i.close, i.high, i.low, i.vol])
    similarity_short_term_data = {'similarity_1_data': similarity_1_data, 'similarity_2_data': similarity_2_data, 'similarity_3_data': similarity_3_data,
                                  'similarity_match_1_data': similarity_match_1_data,'similarity_match_2_data': similarity_match_2_data,'similarity_match_3_data': similarity_match_3_data,
                                  'mark_line': mark_line, 'similarity_match_mark_line_1': similarity_match_mark_line_1,
                                  'similarity_match_mark_line_2': similarity_match_mark_line_2,'similarity_match_mark_line_3': similarity_match_mark_line_3,
                                  'sparkline_data': sparkline_data,
                                  'similarity_1_sparkline_data': similarity_1_sparkline_data,'similarity_2_sparkline_data': similarity_2_sparkline_data,'similarity_3_sparkline_data': similarity_3_sparkline_data,
                                  'similarity_1_table_data': similarity_1_table_data,'similarity_2_table_data': similarity_2_table_data,'similarity_3_table_data': similarity_3_table_data,
                                  'similarity_stock': [{'code': similarity_1_stock.ts_code, 'name': similarity_1_stock.name,'distance':similarity_short_term_result.similarity_1_distance},{'code': similarity_2_stock.ts_code,'name': similarity_2_stock.name,'distance':similarity_short_term_result.similarity_2_distance},{ 'code': similarity_3_stock.ts_code,'name': similarity_3_stock.name,'distance':similarity_short_term_result.similarity_3_distance}],
                                  'trend_description':similarity_short_term_result.similarity_1_trend_description}

    correlation_data = []
    correlation_1_data = []
    correlation_2_data = []
    correlation_3_data = []
    correlation_match_1_data = []
    correlation_match_2_data = []
    correlation_match_3_data = []
    correlation_short_term_result = Model_Correlation_Short_Term.query.filter_by(ts_code=code, trade_date=date).first()
    correlation_1_stock = Stock_Basic.query.filter_by(ts_code=correlation_short_term_result.correlation_1_code).first()
    correlation_2_stock = Stock_Basic.query.filter_by(ts_code=correlation_short_term_result.correlation_2_code).first()
    correlation_3_stock = Stock_Basic.query.filter_by(ts_code=correlation_short_term_result.correlation_3_code).first()
    correlation_1_result = Stock_Daily_Bar.query.filter(
        Stock_Daily_Bar.ts_code == correlation_short_term_result.correlation_1_code,
        Stock_Daily_Bar.trade_date <= correlation_short_term_result.correlation_1_prediction_end_time,).order_by(Stock_Daily_Bar.trade_date.desc()).limit(90).all()
    correlation_2_result = Stock_Daily_Bar.query.filter(
        Stock_Daily_Bar.ts_code == correlation_short_term_result.correlation_2_code,
        Stock_Daily_Bar.trade_date <= correlation_short_term_result.correlation_2_prediction_end_time,).order_by(Stock_Daily_Bar.trade_date.desc()).limit(90).all()
    correlation_3_result = Stock_Daily_Bar.query.filter(
        Stock_Daily_Bar.ts_code == correlation_short_term_result.correlation_3_code,
        Stock_Daily_Bar.trade_date <= correlation_short_term_result.correlation_3_prediction_end_time,).order_by(Stock_Daily_Bar.trade_date.desc()).limit(90).all()
    correlation_1_result.reverse()
    correlation_2_result.reverse()
    correlation_3_result.reverse()
    for i in bar_data[-60:]:
        trade_date = i.trade_date
        correlation_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    for i in correlation_1_result[-30:]:
        factor=bar_data[-1].close/correlation_1_result[-31].close
        trade_date = i.trade_date
        correlation_1_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open*factor, i.close*factor, i.low*factor, i.high*factor,
             i.amount])
    for i in correlation_2_result[-30:]:
        factor=bar_data[-1].close/correlation_2_result[-31].close
        trade_date = i.trade_date
        correlation_2_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open*factor, i.close*factor, i.low*factor, i.high*factor,
             i.amount])
    for i in correlation_3_result[-30:]:
        factor=bar_data[-1].close/correlation_3_result[-31].close
        trade_date = i.trade_date
        correlation_3_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open*factor, i.close*factor, i.low*factor, i.high*factor,
             i.amount])
    correlation_1_data=correlation_data+correlation_1_data
    correlation_2_data = correlation_data + correlation_2_data
    correlation_3_data = correlation_data + correlation_3_data
    for i in correlation_1_result:
        trade_date = i.trade_date
        correlation_match_1_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    for i in correlation_2_result:
        trade_date = i.trade_date
        correlation_match_2_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    for i in correlation_3_result:
        trade_date = i.trade_date
        correlation_match_3_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
    correlation_match_mark_line_1 = [(correlation_short_term_result.correlation_1_matching_start_time[0:4] + '/' + correlation_short_term_result.correlation_1_matching_start_time[4:6] + '/' + correlation_short_term_result.correlation_1_matching_start_time[6:8]),
        (correlation_short_term_result.correlation_1_matching_end_time[0:4] + '/' + correlation_short_term_result.correlation_1_matching_end_time[4:6] + '/' + correlation_short_term_result.correlation_1_matching_end_time[6:8])]
    correlation_match_mark_line_2 = [(correlation_short_term_result.correlation_2_matching_start_time[0:4] + '/' + correlation_short_term_result.correlation_2_matching_start_time[4:6] + '/' + correlation_short_term_result.correlation_2_matching_start_time[6:8]),
        (correlation_short_term_result.correlation_2_matching_end_time[0:4] + '/' + correlation_short_term_result.correlation_2_matching_end_time[4:6] + '/' + correlation_short_term_result.correlation_2_matching_end_time[6:8])]
    correlation_match_mark_line_3 = [(correlation_short_term_result.correlation_3_matching_start_time[0:4] + '/' + correlation_short_term_result.correlation_3_matching_start_time[4:6] + '/' +correlation_short_term_result.correlation_3_matching_start_time[6:8]),
        (correlation_short_term_result.correlation_3_matching_end_time[0:4] + '/' + correlation_short_term_result.correlation_3_matching_end_time[4:6] + '/' + correlation_short_term_result.correlation_3_matching_end_time[6:8])]
    correlation_1_sparkline_data = []
    correlation_2_sparkline_data = []
    correlation_3_sparkline_data = []
    for i in correlation_1_result[-50:]:
        correlation_1_sparkline_data.append(i.pct_chg)
    for i in correlation_2_result[-50:]:
        correlation_2_sparkline_data.append(i.pct_chg)
    for i in correlation_3_result[-50:]:
        correlation_3_sparkline_data.append(i.pct_chg)
    correlation_1_table_data = []
    correlation_2_table_data = []
    correlation_3_table_data = []
    for i in correlation_1_result[-30:]:
        correlation_1_table_data.append([i.pct_chg, i.open, i.close, i.high, i.low, i.vol])
    for i in correlation_2_result[-30:]:
        correlation_2_table_data.append([i.pct_chg, i.open, i.close, i.high, i.low, i.vol])
    for i in correlation_3_result[-30:]:
        correlation_3_table_data.append([i.pct_chg, i.open, i.close, i.high, i.low, i.vol])
    correlation_short_term_data = {'correlation_1_data': correlation_1_data, 'correlation_2_data': correlation_2_data, 'correlation_3_data': correlation_3_data,
                                  'correlation_match_1_data': correlation_match_1_data,'correlation_match_2_data': correlation_match_2_data,'correlation_match_3_data': correlation_match_3_data,
                                  'mark_line': mark_line, 'correlation_match_mark_line_1': correlation_match_mark_line_1,
                                  'correlation_match_mark_line_2': correlation_match_mark_line_2,'correlation_match_mark_line_3': correlation_match_mark_line_3,
                                  'sparkline_data': sparkline_data,
                                  'correlation_1_sparkline_data': correlation_1_sparkline_data,'correlation_2_sparkline_data': correlation_2_sparkline_data,'correlation_3_sparkline_data': correlation_3_sparkline_data,
                                  'correlation_1_table_data': correlation_1_table_data,'correlation_2_table_data': correlation_2_table_data,'correlation_3_table_data': correlation_3_table_data,
                                  'correlation_stock': [{'code': correlation_1_stock.ts_code, 'name': correlation_1_stock.name,'r':correlation_short_term_result.correlation_1_r},{'code': correlation_2_stock.ts_code,'name': correlation_2_stock.name,'r':correlation_short_term_result.correlation_2_r},{ 'code': correlation_3_stock.ts_code,'name': correlation_3_stock.name,'r':correlation_short_term_result.correlation_3_r}],
                                  'trend_description':correlation_short_term_result.correlation_1_trend_description}


    similarity_history_result=Model_Similarity_History.query.filter_by(ts_code=code,trade_date=date).first()
    similarity_history_match_result=Stock_Daily_Bar.query.filter(
        Stock_Daily_Bar.ts_code == code,
        Stock_Daily_Bar.trade_date <= similarity_history_result.prediction_end_time,).order_by(Stock_Daily_Bar.trade_date.desc()).limit(90).all()
    similarity_history_match_result.reverse()
    similarity_history_match_data=[]
    similarity_history_match_sparkline_data=[]
    for i in similarity_history_match_result:
        trade_date = i.trade_date
        similarity_history_match_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount])
        similarity_history_match_sparkline_data.append(i.pct_chg)
    similarity_history_mark_line=[(similarity_history_result.matching_start_time[0:4] + '/' + similarity_history_result.matching_start_time[4:6] + '/' + similarity_history_result.matching_start_time[6:8]),
        (similarity_history_result.matching_end_time[0:4] + '/' + similarity_history_result.matching_end_time[4:6] + '/' + similarity_history_result.matching_end_time[6:8])]
    similarity_history_match_date=[(date[0:4] + '/' + date[4:6] + '/' + date[6:8]),
                                   (similarity_history_result.matching_end_time[0:4] + '/' + similarity_history_result.matching_end_time[4:6] + '/' + similarity_history_result.matching_end_time[6:8])]
    similarity_history_sparkline_data=[]
    for i in bar_data[-60:]:
        similarity_history_sparkline_data.append(i.pct_chg)
    similarity_history_sparkline_data.extend([None]*30)
    similarity_history_table_data = []
    for i in similarity_history_match_result[-30:]:
        similarity_history_table_data.append([i.pct_chg, i.open, i.close, i.high, i.low, i.vol])
    similarity_history_data={'similarity_history_match_data':similarity_history_match_data,'mark_line':similarity_history_mark_line,'match_date':similarity_history_match_date,
                             'similarity_history_match_sparkline_data':similarity_history_match_sparkline_data,'sparkline_data':similarity_history_sparkline_data,
                             'similarity_history_table_data':similarity_history_table_data}


    bar_data_for_state_transition_result=Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == code, Stock_Daily_Bar.trade_date <= date,
                                            ).order_by(Stock_Daily_Bar.trade_date.desc()).limit(300).all()
    state_transition_result=Model_State_Transition.query.filter(Model_State_Transition.ts_code==code,Model_State_Transition.trade_date<=date).order_by(Model_State_Transition.trade_date.desc()).limit(300).all()
    bar_data_for_state_transition_result.reverse()
    state_transition_result.reverse()
    today_state_transition_data={'s_rise_rate':state_transition_result[-1].s_rise_rate,'s_maintain_rate':state_transition_result[-1].s_maintain_rate,'s_fall_rate':state_transition_result[-1].s_fall_rate,
                                 'l_rise_rate': state_transition_result[-1].l_rise_rate,'l_maintain_rate': state_transition_result[-1].l_maintain_rate,'l_fall_rate': state_transition_result[-1].l_fall_rate}
    s_rise_sparkline_data=[]
    s_fall_sparkline_data=[]
    l_rise_sparkline_data=[]
    l_fall_sparkline_data=[]
    state_transition_line_data=[]
    for i in state_transition_result[-60:]:
        s_rise_sparkline_data.append(i.s_rise_rate)
        s_fall_sparkline_data.append(i.s_fall_rate)
        l_rise_sparkline_data.append(i.l_rise_rate)
        l_fall_sparkline_data.append(i.l_fall_rate)
    for i,j in zip(bar_data_for_state_transition_result,state_transition_result):
        trade_date = i.trade_date
        state_transition_line_data.append(
            [(trade_date[0:4] + '/' + trade_date[4:6] + '/' + trade_date[6:8]), i.open, i.close, i.low, i.high,
             i.amount,j.s_rise_rate,j.s_fall_rate,j.l_rise_rate,j.l_fall_rate])
    state_transition_data={'state_transition_line_data':state_transition_line_data,'today_state_transition_data':today_state_transition_data,
                           's_rise_sparkline_data':s_rise_sparkline_data,'s_fall_sparkline_data':s_fall_sparkline_data,'l_rise_sparkline_data':l_rise_sparkline_data,
                           'l_fall_sparkline_data': l_fall_sparkline_data}

    return jsonify({'today_bar_data': today_bar_data, 'today_basic_data': today_basic_data,
                    'trade_point_data': {'line_data': trade_point_line_data, 'aggressive': aggressive_trade_point,
                                         'steady': steady_trade_point, 'aggressive_requirement': aggressive_requirement,
                                         'steady_requirement': steady_requirement},
                    'trend_forecast_data': {'first_vote': first_vote, 'second_vote': second_vote,
                                            'third_vote': third_vote,'first_change': trend_forecast_result.first_change,
                                            'second_change': trend_forecast_result.second_change,'third_change': trend_forecast_result.third_change},
                    'similarity_short_term_data': similarity_short_term_data,'correlation_short_term_data':correlation_short_term_data,
                    'similarity_history_data':similarity_history_data,
                    'state_transition_data':state_transition_data})



#####################################################
import tushare as ts
@stock_prediction.route('api_qjzn',methods=['GET'])
def api_qjzn():
    code = request.args.get("code")
    date = request.args.get("date")
    result_qjzn = my_session.query(qjzn).filter(qjzn.stock_code == code).first()
    result_jccwzb = my_session.query(jccwzb).filter(jccwzb.ts_code == code).first()
    data = {
        'date':date,
        'code':code,
        'name':result_jccwzb.sec_name,
        'industry':[result_qjzn.industry2],
        'concept':tuple(result_qjzn.concept.split(";")),
        'region':[result_qjzn.province,result_qjzn.city],
        'zijin':{
            'industry':{
                'name':[],
                'value':[],
                'change':[],
            },
            'concept':{
                'name':[],
                'value':[],
                'change':[],
            },
            'region':{
                'name':[],
                'value':[],
                'change':[],
            },
        },
        'huanshou':{
            'industry':{
                'name':[],
                'value':[],
                'change':[],
            },
            'concept':{
                'name':[],
                'value':[],
                'change':[],
            },
            'region':{
                'name':[],
                'value':[],
                'change':[],
            },
        },
        'zhangdie':{
            'industry':{
                'name':[],
                'value':[],
                'change':[],
            },
            'concept':{
                'name':[],
                'value':[],
                'change':[],
            },
            'region':{
                'name':[],
                'value':[],
                'change':[],
            },

        },
        'shizhi':{
             'industry':{
                'name':[],
                'value':[],
                'change':[],
            },
            'concept':{
                'name':[],
                'value':[],
                'change':[],
            },
            'region':{
                'name':[],
                'value':[],
                'change':[],
            },
        },
        'guzhi':{},
        'gudong':{},
    }
    pro = ts.pro_api()
    cal = pro.trade_cal(exchange='',fields='cal_date,pretrade_date,is_open', start_date=date, end_date=date)
    pretrade_date = cal.pretrade_date[0]
    # 获取行业数据
    result = my_session.query(bkqj_cndtqj).filter(bkqj_cndtqj.date == date).order_by(bkqj_cndtqj.industry_name.desc()).all()
    pre_result = my_session.query(bkqj_cndtqj).filter(bkqj_cndtqj.date == pretrade_date).order_by(bkqj_cndtqj.industry_name.desc()).all()
    # 资金
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].transaction_capital - pre_result[i].transaction_capital)/result[i].transaction_capital)*100
        tmp[result[i].industry_name] = [result[i].transaction_capital,pre_result[i].transaction_capital,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['zijin']['industry']['name'].append(tmp_sorted[i][0])
        data['zijin']['industry']['value'].append(tmp_sorted[i][1][0]/100000000)
        data['zijin']['industry']['change'].append(round(tmp_sorted[i][1][2],2))
    # 换手
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].ave_turnover_rate - pre_result[i].ave_turnover_rate)/result[i].ave_turnover_rate)*100
        tmp[result[i].industry_name] = [result[i].ave_turnover_rate,pre_result[i].ave_turnover_rate,change]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['huanshou']['industry']['name'].append(tmp_sorted[i][0])
        data['huanshou']['industry']['value'].append(round(tmp_sorted[i][1][0],2))
        data['huanshou']['industry']['change'].append(round(tmp_sorted[i][1][2],2))
    # 涨跌
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].ave_up_downs - pre_result[i].ave_up_downs)/result[i].ave_up_downs)*100
        tmp[result[i].industry_name] = [result[i].ave_up_downs,pre_result[i].ave_up_downs,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['zhangdie']['industry']['name'].append(tmp_sorted[i][0])
        data['zhangdie']['industry']['value'].append(round(tmp_sorted[i][1][0],2))
        data['zhangdie']['industry']['change'].append(round(tmp_sorted[i][1][2],2))
    # 市值
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].cur_market_value - pre_result[i].cur_market_value)/result[i].cur_market_value)*100
        tmp[result[i].industry_name] = [result[i].cur_market_value,pre_result[i].cur_market_value,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['shizhi']['industry']['name'].append(tmp_sorted[i][0])
        data['shizhi']['industry']['value'].append(tmp_sorted[i][1][0]/100000000000)
        data['shizhi']['industry']['change'].append(round(tmp_sorted[i][1][2],2))

    # 获取概念数据
    result = my_session.query(bkqj_cndtqj_conceptual).filter(bkqj_cndtqj_conceptual.date == date).order_by(bkqj_cndtqj_conceptual.conceptual_name.desc()).all()
    pre_result = my_session.query(bkqj_cndtqj_conceptual).filter(bkqj_cndtqj_conceptual.date == pretrade_date).order_by(bkqj_cndtqj_conceptual.conceptual_name.desc()).all()
    # 资金
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].transaction_capital - pre_result[i].transaction_capital)/result[i].transaction_capital)*100
        tmp[result[i].conceptual_name] = [result[i].transaction_capital,pre_result[i].transaction_capital,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['zijin']['concept']['name'].append(tmp_sorted[i][0])
        data['zijin']['concept']['value'].append(tmp_sorted[i][1][0]/100000000)
        data['zijin']['concept']['change'].append(round(tmp_sorted[i][1][2],2))
    # 换手
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].ave_turnover_rate - pre_result[i].ave_turnover_rate)/result[i].ave_turnover_rate)*100
        tmp[result[i].conceptual_name] = [result[i].ave_turnover_rate,pre_result[i].ave_turnover_rate,change]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['huanshou']['concept']['name'].append(tmp_sorted[i][0])
        data['huanshou']['concept']['value'].append(round(tmp_sorted[i][1][0],2))
        data['huanshou']['concept']['change'].append(round(tmp_sorted[i][1][2],2))
    # 涨跌
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].ave_up_downs - pre_result[i].ave_up_downs)/result[i].ave_up_downs)*100
        tmp[result[i].conceptual_name] = [result[i].ave_up_downs,pre_result[i].ave_up_downs,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['zhangdie']['concept']['name'].append(tmp_sorted[i][0])
        data['zhangdie']['concept']['value'].append(round(tmp_sorted[i][1][0],2))
        data['zhangdie']['concept']['change'].append(round(tmp_sorted[i][1][2],2))
    # 市值
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].cur_market_value - pre_result[i].cur_market_value)/result[i].cur_market_value)*100
        tmp[result[i].conceptual_name] = [result[i].cur_market_value,pre_result[i].cur_market_value,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['shizhi']['concept']['name'].append(tmp_sorted[i][0])
        data['shizhi']['concept']['value'].append(tmp_sorted[i][1][0]/100000000000)
        data['shizhi']['concept']['change'].append(round(tmp_sorted[i][1][2],2))
    # 获取地域数据
    result = my_session.query(bkqj_cndtqj_region).filter(bkqj_cndtqj_region.date == date).order_by(bkqj_cndtqj_region.region_name.desc()).all()
    pre_result = my_session.query(bkqj_cndtqj_region).filter(bkqj_cndtqj_region.date == pretrade_date).order_by(bkqj_cndtqj_region.region_name.desc()).all()
    # 资金
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].transaction_capital - pre_result[i].transaction_capital)/result[i].transaction_capital)*100
        tmp[result[i].region_name] = [result[i].transaction_capital,pre_result[i].transaction_capital,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['zijin']['region']['name'].append(tmp_sorted[i][0])
        data['zijin']['region']['value'].append(tmp_sorted[i][1][0]/100000000)
        data['zijin']['region']['change'].append(round(tmp_sorted[i][1][2],2))
    # 换手
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].ave_turnover_rate - pre_result[i].ave_turnover_rate)/result[i].ave_turnover_rate)*100
        tmp[result[i].region_name] = [result[i].ave_turnover_rate,pre_result[i].ave_turnover_rate,change]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['huanshou']['region']['name'].append(tmp_sorted[i][0])
        data['huanshou']['region']['value'].append(round(tmp_sorted[i][1][0],2))
        data['huanshou']['region']['change'].append(round(tmp_sorted[i][1][2],2))
    # 涨跌
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].ave_up_downs - pre_result[i].ave_up_downs)/result[i].ave_up_downs)*100
        tmp[result[i].region_name] = [result[i].ave_up_downs,pre_result[i].ave_up_downs,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['zhangdie']['region']['name'].append(tmp_sorted[i][0])
        data['zhangdie']['region']['value'].append(round(tmp_sorted[i][1][0],2))
        data['zhangdie']['region']['change'].append(round(tmp_sorted[i][1][2],2))
    # 市值
    tmp = {
    }
    for i in range(0,len(result)):
        change = ((result[i].cur_market_value - pre_result[i].cur_market_value)/result[i].cur_market_value)*100
        tmp[result[i].region_name] = [result[i].cur_market_value,pre_result[i].cur_market_value,change,2]
    # 排序存入data
    tmp_sorted = sorted(tmp.items(), key=lambda d: d[1], reverse=True)
    for i in range(0,len(tmp_sorted)):
        data['shizhi']['region']['name'].append(tmp_sorted[i][0])
        data['shizhi']['region']['value'].append(tmp_sorted[i][1][0]/100000000000)
        data['shizhi']['region']['change'].append(round(tmp_sorted[i][1][2],2))

    return jsonify(data)


@stock_prediction.route('api_cwzb_zycwzb', methods=('GET', 'POST'))
def api_cwzb_zycwzb():
    # ts_code =  request.form.get('ts_code')
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(8)
    data_1 = {}
    data_1['the_date'] = []
    data_1['eps_basic_is'] = []
    data_1['net_asset_per'] = []
    data_1['net_cash_flows_oper_act_per'] = []
    data_1['main_oper_rev']=[]
    data_1['main_oper_profit'] = []
    data_1['oper_profit'] = []
    data_1['net_invest_inc'] = []
    data_1['net_non_oper_income'] = []
    data_1['tot_profit'] = []
    data_1['net_profit_is'] = []
    data_1[' net_profit_is_excluded'] = []
    data_1['net_cash_flows_oper_act'] = []
    data_1['net_incr_cash_cash_equ_dm'] = []
    data_1['tot_assets'] = []
    data_1['tot_cur_assets'] = []
    data_1['tot_liab'] = []
    data_1['tot_cur_liab'] = []
    data_1['tot_equity'] = []
    data_1['rate_rec_on_net_asset'] = []

    for i in result1:
        if ((i.the_date.day==31)and(i.the_date.month==12)) or ((i.the_date.day==31)and(i.the_date.month==3)) or ((i.the_date.day==30)and(i.the_date.month==6)) or ((i.the_date.day==30)and(i.the_date.month==9)):
            data_1['eps_basic_is'].append(i.eps_basic_is)
            data_1['the_date'].append(str(i.the_date.year) + '-' + str(i.the_date.month) + '-' + str(i.the_date.day))
            data_1['net_asset_per'].append(i.net_asset_per)
            data_1['net_cash_flows_oper_act_per'].append(i.net_cash_flows_oper_act_per)
            data_1['main_oper_rev'].append(i.main_oper_rev/10000)
            data_1['main_oper_profit'].append(i.main_oper_profit/10000)
            data_1['oper_profit'].append(i.oper_profit/10000)
            data_1['net_invest_inc'].append(i.net_invest_inc/10000)
            data_1['net_non_oper_income'].append(i.net_non_oper_income/10000)
            data_1['tot_profit'].append(i.tot_profit/10000)
            data_1['net_profit_is'].append(i.net_profit_is/10000)
            data_1[' net_profit_is_excluded'].append(i.net_profit_is_excluded/10000)
            data_1['net_cash_flows_oper_act'].append(i.net_cash_flows_oper_act/10000)
            data_1['net_incr_cash_cash_equ_dm'].append(i.net_incr_cash_cash_equ_dm/10000)
            data_1['tot_assets'].append(i.tot_assets/10000)
            data_1['tot_cur_assets'].append(i.tot_cur_assets/10000)
            data_1['tot_liab'].append(i.tot_liab/10000)
            data_1['tot_cur_liab'].append(i.tot_cur_liab/10000)
            data_1['tot_equity'].append(i.tot_equity/10000)
            data_1['rate_rec_on_net_asset'].append(i.rate_rec_on_net_asset)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_zycwzb_year', methods=('GET', 'POST'))
def api_cwzb_zycwzb_year():
    # ts_code =  request.form.get('ts_code')
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(40)
    data_1 = {}
    data_1['the_date'] = []
    data_1['eps_basic_is'] = []
    data_1['net_asset_per'] = []
    data_1['net_cash_flows_oper_act_per'] = []
    data_1['main_oper_rev']=[]
    data_1['main_oper_profit'] = []
    data_1['oper_profit'] = []
    data_1['net_invest_inc'] = []
    data_1['net_non_oper_income'] = []
    data_1['tot_profit'] = []
    data_1['net_profit_is'] = []
    data_1[' net_profit_is_excluded'] = []
    data_1['net_cash_flows_oper_act'] = []
    data_1['net_incr_cash_cash_equ_dm'] = []
    data_1['tot_assets'] = []
    data_1['tot_cur_assets'] = []
    data_1['tot_liab'] = []
    data_1['tot_cur_liab'] = []
    data_1['tot_equity'] = []
    data_1['rate_rec_on_net_asset'] = []

    for i in result1:
        if ((i.the_date.day==31)and(i.the_date.month==12)):
            data_1['eps_basic_is'].append(i.eps_basic_is)
            data_1['the_date'].append(str(i.the_date.year) + '-' + str(i.the_date.month) + '-' + str(i.the_date.day))
            data_1['net_asset_per'].append(i.net_asset_per)
            data_1['net_cash_flows_oper_act_per'].append(i.net_cash_flows_oper_act_per)
            data_1['main_oper_rev'].append(i.main_oper_rev / 10000)
            data_1['main_oper_profit'].append(i.main_oper_profit / 10000)
            data_1['oper_profit'].append(i.oper_profit / 10000)
            data_1['net_invest_inc'].append(i.net_invest_inc / 10000)
            data_1['net_non_oper_income'].append(i.net_non_oper_income / 10000)
            data_1['tot_profit'].append(i.tot_profit / 10000)
            data_1['net_profit_is'].append(i.net_profit_is / 10000)
            data_1[' net_profit_is_excluded'].append(i.net_profit_is_excluded / 10000)
            data_1['net_cash_flows_oper_act'].append(i.net_cash_flows_oper_act / 10000)
            data_1['net_incr_cash_cash_equ_dm'].append(i.net_incr_cash_cash_equ_dm / 10000)
            data_1['tot_assets'].append(i.tot_assets / 10000)
            data_1['tot_cur_assets'].append(i.tot_cur_assets / 10000)
            data_1['tot_liab'].append(i.tot_liab / 10000)
            data_1['tot_cur_liab'].append(i.tot_cur_liab / 10000)
            data_1['tot_equity'].append(i.tot_equity / 10000)
            data_1['rate_rec_on_net_asset'].append(i.rate_rec_on_net_asset)
    return jsonify(data_1)


@stock_prediction.route('api_cwzb_ylnl', methods=('GET', 'POST'))
def api_cwzb_ylnl():
    # ts_code =  request.form.get('ts_code')
    # result1 = jccwzb.query.filter(ts_code == ts_code).all()
    result1 = jccwzb.query.filter_by(ts_code="000001.SZ").order_by(jccwzb.date.desc()).limit(8)
    data_1 = {}
    data_1['date'] = []
    data_1['rate_return_on_tot_asset'] = []
    data_1['rate_return_on_cost'] = []
    data_1['net_profit_margin'] = []
    data_1['rate_return_on_net_asset']=[]
    data_1['three_cost_proportion'] = []
    data_1['pro_margin_main_business'] = []
    data_1['oper_profit_margin'] = []
    data_1['rate_return_on_equity'] = []
    data_1['rate_return_on_asset'] = []
    data_1['non_main_proportion'] = []
    data_1['rate_net_return_on_tot_asset'] = []
    data_1['rate_gross_sales_interest'] = []
    data_1['cost_rate_main_business'] = []
    data_1['rate_equity_reward'] = []
    data_1['ratio_main_profit'] = []


    for i in result1:
        data_1['rate_return_on_tot_asset'].append(i.rate_return_on_tot_asset*100)
        data_1['date'].append(i.date)
        data_1['rate_return_on_cost'].append(i.rate_return_on_cost)
        data_1['net_profit_margin'].append(i.net_profit_margin)
        data_1['rate_return_on_net_asset'].append(i.rate_return_on_net_asset*100)
        data_1['three_cost_proportion'].append(i.three_cost_proportion)
        data_1['pro_margin_main_business'].append(i.pro_margin_main_business*100)
        data_1['oper_profit_margin'].append(i.oper_profit_margin)
        data_1['rate_return_on_equity'].append(i.rate_return_on_equity)
        data_1['rate_return_on_asset'].append(i.rate_return_on_asset*100)
        data_1['non_main_proportion'].append(i.non_main_proportion*100)
        data_1['rate_net_return_on_tot_asset'].append(i.rate_net_return_on_tot_asset*100)
        data_1['cost_rate_main_business'].append(i.cost_rate_main_business)
        data_1['rate_equity_reward'].append(i.rate_equity_reward)
        data_1['ratio_main_profit'].append(i.ratio_main_profit)
        data_1['rate_gross_sales_interest'].append(i.rate_gross_sales_interest)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_chnl', methods=('GET', 'POST'))
def api_cwzb_chnl():
    # code = request.args.get('code')
    result1 = jccwzb.query.filter_by(ts_code="000001.SZ").order_by(jccwzb.date.desc()).limit(8)
    data_1 = {}
    data_1['date'] = []
    data_1['ratio_current'] = []
    data_1['ratio_long_debts_working_captial'] = []
    data_1['ratio_long_assets_long_captial'] = []
    data_1['ratio_liquidation_value']=[]
    data_1['ratio_quick'] = []
    data_1['ratio_sh_equity'] = []
    data_1['ratio_capitalization'] = []
    data_1['ratio_share_equity'] = []
    data_1['ratio_cash'] = []
    data_1['ratio_long_debt'] = []
    data_1['ration_net_value_fixed_assets'] = []
    data_1['ratio_interest_coverage'] = []
    data_1['ration_sh_right_fixed_assets'] = []
    data_1['ratio_capital_immobilization'] = []
    data_1['ratio_asset_liability'] = []
    data_1['ratio_debt_right'] = []
    data_1['ratio_property_right'] = []


    for i in result1:
        data_1['ratio_current'].append(i.ratio_current)
        data_1['date'].append(i.date)
        data_1['ratio_long_debts_working_captial'].append(i.ratio_long_debts_working_captial)
        data_1['ratio_long_assets_long_captial'].append(i.ratio_long_assets_long_captial)
        data_1['ratio_liquidation_value'].append(i.ratio_liquidation_value)
        data_1['ratio_quick'].append(i.ratio_quick)
        data_1['ratio_sh_equity'].append(i.ratio_sh_equity)
        data_1['ratio_capitalization'].append(i.ratio_capitalization)
        data_1['ratio_share_equity'].append(i.ratio_share_equity*100)
        data_1['ratio_cash'].append(i.ratio_cash)
        data_1['ratio_long_debt'].append(i.ratio_long_debt)
        data_1['ration_net_value_fixed_assets'].append(i.ration_net_value_fixed_assets)
        data_1['ratio_interest_coverage'].append(i.ratio_interest_coverage)
        data_1['ration_sh_right_fixed_assets'].append(i.ration_sh_right_fixed_assets*100)
        data_1['ratio_capital_immobilization'].append(i.ratio_capital_immobilization)
        data_1['ratio_asset_liability'].append(i.ratio_asset_liability)
        data_1['ratio_debt_right'].append(i.ratio_debt_right)
        data_1['ratio_property_right'].append(i.ratio_property_right)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_cznl', methods=('GET', 'POST'))
def api_cwzb_cznl():
    # ts_code =  request.form.get('ts_code')
    # result1 = jccwzb.query.filter(ts_code == ts_code).all()
    result1 = jccwzb.query.filter_by(ts_code="000001.SZ").order_by(jccwzb.date.desc()).limit(8)
    data_1 = {}
    data_1['date'] = []
    data_1['growth_rate_main_business_income'] = []
    data_1['growth_rate_net_profit'] = []
    data_1['growth_rate_net_assets'] = []
    data_1['growth_rate_tot_assets']=[]

    for i in result1:
        data_1['growth_rate_main_business_income'].append(i.growth_rate_main_business_income)
        data_1['date'].append(i.date)
        data_1['growth_rate_net_profit'].append(i.growth_rate_net_profit)
        data_1['growth_rate_net_assets'].append(i.growth_rate_net_assets)
        data_1['growth_rate_tot_assets'].append(i.growth_rate_tot_assets)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_yynl', methods=('GET', 'POST'))
def api_cwzb_yynl():
    # ts_code =  request.form.get('ts_code')
    result1 = jccwzb.query.filter_by(ts_code="000001.SZ").order_by(jccwzb.date.desc()).limit(8)
    data_1 = {}
    data_1['date'] = []
    data_1['rate_receivable_turnover'] = []
    data_1['days_inventory_turnover_oper_income'] = []
    data_1['rate_assets_oper_cash_flow'] = []
    data_1['days_receivable_turnover']=[]
    data_1['days_tot_assets_turnover'] = []
    data_1['ratio_oper_cash_net_profit'] = []
    data_1['ratio_inventory_turnover'] = []
    data_1['ratio_current_assets_turnover'] = []
    data_1['ratio_oper_cash_debt'] = []
    data_1['ratio_fixed_assets_turnover'] = []
    data_1['days_current_assets_turnover'] = []
    data_1['ratio_cash_flow'] = []
    data_1['ratio_tot_assets_turnover'] = []
    data_1['ratio_oper_cash_income'] = []

    for i in result1:
        data_1['rate_receivable_turnover'].append(i.rate_receivable_turnover)
        data_1['date'].append(i.date)
        data_1['days_inventory_turnover_oper_income'].append(i.days_inventory_turnover_oper_income)
        data_1['rate_assets_oper_cash_flow'].append(i.rate_assets_oper_cash_flow*100)
        data_1['days_receivable_turnover'].append(i.days_receivable_turnover)
        data_1['days_tot_assets_turnover'].append(i.days_tot_assets_turnover)
        data_1['ratio_oper_cash_net_profit'].append(i.ratio_oper_cash_net_profit*100)
        data_1['ratio_inventory_turnover'].append(i.ratio_inventory_turnover)
        data_1['ratio_current_assets_turnover'].append(i.ratio_current_assets_turnover)
        data_1['ratio_oper_cash_debt'].append(i.ratio_oper_cash_debt*100)
        data_1['ratio_fixed_assets_turnover'].append(i.ratio_fixed_assets_turnover)
        data_1['days_current_assets_turnover'].append(i.days_current_assets_turnover)
        data_1['ratio_cash_flow'].append(i.ratio_cash_flow*100)
        data_1['ratio_tot_assets_turnover'].append(i.ratio_tot_assets_turnover)
        data_1['ratio_oper_cash_income'].append(i.ratio_oper_cash_income*100)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_lrbzy', methods=('GET', 'POST'))
def api_cwzb_lrbzy():
    # ts_code =  request.form.get('ts_code')
    # result1 = jccwsj.query.filter(ts_code == ts_code).all()
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(8)
    data_1 = {}
    data_1['the_date'] = []
    data_1['oper_rev'] = []
    data_1['oper_profit'] = []
    data_1['income_tax_expenses'] = []
    data_1['eps_basic_is']=[]
    data_1['oper_cost'] = []
    data_1['tot_profit'] = []
    data_1['net_profit_is'] = []

    for i in result1:
        if ((i.the_date.day == 31) and (i.the_date.month == 12)) or (
                (i.the_date.day == 31) and (i.the_date.month == 3)) or (
                (i.the_date.day == 30) and (i.the_date.month == 6)) or (
                (i.the_date.day == 30) and (i.the_date.month == 9)):
            data_1['oper_rev'].append(i.oper_rev/10000)
            data_1['the_date'].append(str(i.the_date.year) + '/' + str(i.the_date.month) + '/' + str(i.the_date.day))
            data_1['oper_profit'].append(i.oper_profit/10000)
            data_1['income_tax_expenses'].append(i.income_tax_expenses)
            data_1['eps_basic_is'].append(i.eps_basic_is)
            data_1['oper_cost'].append(i.oper_cost/100000)
            data_1['tot_profit'].append(i.tot_profit/10000)
            data_1['net_profit_is'].append(i.net_profit_is/10000)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_lrbzy_year', methods=('GET', 'POST'))
def api_cwzb_lrbzy_year():
    # ts_code =  request.form.get('ts_code')
    # result1 = jccwsj.query.filter(ts_code == ts_code).all()
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(40)
    data_1 = {}
    data_1['the_date'] = []
    data_1['oper_rev'] = []
    data_1['oper_profit'] = []
    data_1['income_tax_expenses'] = []
    data_1['eps_basic_is']=[]
    data_1['oper_cost'] = []
    data_1['tot_profit'] = []
    data_1['net_profit_is'] = []

    for i in result1:
        if ((i.the_date.day == 31) and (i.the_date.month == 12)):
            data_1['oper_rev'].append(i.oper_rev / 10000)
            data_1['the_date'].append(str(i.the_date.year) + '/' + str(i.the_date.month) + '/' + str(i.the_date.day))
            data_1['oper_profit'].append(i.oper_profit / 10000)
            data_1['income_tax_expenses'].append(i.income_tax_expenses)
            data_1['eps_basic_is'].append(i.eps_basic_is)
            data_1['oper_cost'].append(i.oper_cost / 100000)
            data_1['tot_profit'].append(i.tot_profit / 10000)
            data_1['net_profit_is'].append(i.net_profit_is / 10000)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_zcfzbzy', methods=('GET', 'POST'))
def api_cwzb_zcfzbzy():
    # ts_code =  request.form.get('ts_code')
    # result1 = jccwsj.query.filter(ts_code == ts_code).all()
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(8)
    data_1 = {}
    data_1['the_date'] = []
    data_1['monetary_cap'] = []
    data_1['tot_cur_assets'] = []
    data_1['tot_cur_liab'] = []
    data_1['sh_rights']=[]
    data_1['long_term_rec'] = []
    data_1['tot_equity'] = []
    data_1['tot_non_cur_liab'] = []
    data_1['inventories'] = []
    data_1['tot_assets'] = []
    data_1['net_fixed_assets'] = []

    for i in result1:
        if ((i.the_date.day == 31) and (i.the_date.month == 12)) or (
                (i.the_date.day == 31) and (i.the_date.month == 3)) or (
                (i.the_date.day == 30) and (i.the_date.month == 6)) or (
                (i.the_date.day == 30) and (i.the_date.month == 9)):
            data_1['monetary_cap'].append(i.monetary_cap/10000)
            data_1['the_date'].append(str(i.the_date.year) + '/' + str(i.the_date.month) + '/' + str(i.the_date.day))
            data_1['tot_cur_assets'].append(i.tot_cur_assets/10000)
            data_1['tot_cur_liab'].append(i.tot_cur_liab/10000)
            data_1['sh_rights'].append(i.sh_rights/10000)
            data_1['long_term_rec'].append(i.long_term_rec/10000)
            data_1['tot_equity'].append(i.tot_equity/10000)
            data_1['tot_non_cur_liab'].append(i.tot_non_cur_liab/10000)
            data_1['inventories'].append(i.inventories/10000)
            data_1['tot_assets'].append(i.tot_assets/10000)
            data_1['net_fixed_assets'].append(i.net_fixed_assets/10000)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_zcfzbzy_year', methods=('GET', 'POST'))
def api_cwzb_zcfzbzy_year():
    # ts_code =  request.form.get('ts_code')
    # result1 = jccwsj.query.filter(ts_code == ts_code).all()
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(40)
    data_1 = {}
    data_1['the_date'] = []
    data_1['monetary_cap'] = []
    data_1['tot_cur_assets'] = []
    data_1['tot_cur_liab'] = []
    data_1['sh_rights']=[]
    data_1['long_term_rec'] = []
    data_1['tot_equity'] = []
    data_1['tot_non_cur_liab'] = []
    data_1['inventories'] = []
    data_1['tot_assets'] = []
    data_1['net_fixed_assets'] = []

    for i in result1:
        if ((i.the_date.day == 31) and (i.the_date.month == 12)):
            data_1['monetary_cap'].append(i.monetary_cap / 10000)
            data_1['the_date'].append(str(i.the_date.year) + '/' + str(i.the_date.month) + '/' + str(i.the_date.day))
            data_1['tot_cur_assets'].append(i.tot_cur_assets / 10000)
            data_1['tot_cur_liab'].append(i.tot_cur_liab / 10000)
            data_1['sh_rights'].append(i.sh_rights / 10000)
            data_1['long_term_rec'].append(i.long_term_rec / 10000)
            data_1['tot_equity'].append(i.tot_equity / 10000)
            data_1['tot_non_cur_liab'].append(i.tot_non_cur_liab / 10000)
            data_1['inventories'].append(i.inventories / 10000)
            data_1['tot_assets'].append(i.tot_assets / 10000)
            data_1['net_fixed_assets'].append(i.net_fixed_assets / 10000)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_xjjlbzy', methods=('GET', 'POST'))
def api_cwzb_xjjlbzy():
    # ts_code =  request.form.get('ts_code')
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(8)
    data_1 = {}
    data_1['the_date'] = []
    data_1['cash_cash_equ_beg_period'] = []
    data_1['net_cash_flows_fnc_act'] = []
    data_1['net_cash_flows_oper_act'] = []
    data_1['net_incr_cash_cash_equ_dm']=[]
    data_1['net_cash_flows_inv_act'] = []
    data_1['cash_cash_equ_end_period'] = []

    for i in result1:
        if ((i.the_date.day == 31) and (i.the_date.month == 12)) or (
                (i.the_date.day == 31) and (i.the_date.month == 3)) or (
                (i.the_date.day == 30) and (i.the_date.month == 6)) or (
                (i.the_date.day == 30) and (i.the_date.month == 9)):
            data_1['cash_cash_equ_beg_period'].append(i.cash_cash_equ_beg_period/10000)
            data_1['the_date'].append(str(i.the_date.year) + '/' + str(i.the_date.month) + '/' + str(i.the_date.day))
            data_1['net_cash_flows_fnc_act'].append(i.net_cash_flows_fnc_act/10000)
            data_1['net_cash_flows_oper_act'].append(i.net_cash_flows_oper_act/10000)
            data_1['net_incr_cash_cash_equ_dm'].append(i.net_incr_cash_cash_equ_dm/10000)
            data_1['net_cash_flows_inv_act'].append(i.net_cash_flows_inv_act/10000)
            data_1['cash_cash_equ_end_period'].append(i.cash_cash_equ_end_period/10000)
    return jsonify(data_1)

@stock_prediction.route('api_cwzb_xjjlbzy_year', methods=('GET', 'POST'))
def api_cwzb_xjjlbzy_year():
    # ts_code =  request.form.get('ts_code')
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(40)
    data_1 = {}
    data_1['the_date'] = []
    data_1['cash_cash_equ_beg_period'] = []
    data_1['net_cash_flows_fnc_act'] = []
    data_1['net_cash_flows_oper_act'] = []
    data_1['net_incr_cash_cash_equ_dm']=[]
    data_1['net_cash_flows_inv_act'] = []
    data_1['cash_cash_equ_end_period'] = []

    for i in result1:
        if ((i.the_date.day == 31) and (i.the_date.month == 12)) :
            data_1['cash_cash_equ_beg_period'].append(i.cash_cash_equ_beg_period / 10000)
            data_1['the_date'].append(str(i.the_date.year) + '/' + str(i.the_date.month) + '/' + str(i.the_date.day))
            data_1['net_cash_flows_fnc_act'].append(i.net_cash_flows_fnc_act / 10000)
            data_1['net_cash_flows_oper_act'].append(i.net_cash_flows_oper_act / 10000)
            data_1['net_incr_cash_cash_equ_dm'].append(i.net_incr_cash_cash_equ_dm / 10000)
            data_1['net_cash_flows_inv_act'].append(i.net_cash_flows_inv_act / 10000)
            data_1['cash_cash_equ_end_period'].append(i.cash_cash_equ_end_period / 10000)
    return jsonify(data_1)

@stock_prediction.route('api_cwbg_zhzb', methods=('GET', 'POST'))
def api_cwbg_zhzb():
    result1 = jccwsj.query.filter_by(ts_code="000001.SZ").order_by(jccwsj.the_date.desc()).limit(8)
    result2 = jccwzb.query.filter_by(ts_code="000001.SZ").order_by(jccwzb.date.desc()).limit(8)
    data_1 = {}
    data_1[1]=[]
    data_1[2]=[]
    data_1[3]=[]
    data_1[4]=[]
    data_1[5]=[]
    data_1[6]=[]
    data_1[7]=[]
    data_1[8]=[]
    a=1
    for i in result1:
        if  a<9 :
            data_1[a].append(str(i.the_date.year) + '/' + str(i.the_date.month) + '/' + str(i.the_date.day))
            data_1[a].append(i.eps_basic_is)
            data_1[a].append(i.net_asset_per)
            data_1[a].append(i.eps_diluted_is)
            a=a+1
    a=1
    for i in result2:
        if a<9 :
            data_1[a].append(i.rate_return_on_equity)
            data_1[a].append(i.ratio_current)
            data_1[a].append(i.ratio_quick)
            data_1[a].append(i.rate_receivable_turnover)
            data_1[a].append(i.ratio_asset_liability)
            data_1[a].append(i.rate_net_return_on_tot_asset)
            data_1[a].append(i.rate_return_on_asset)
            data_1[a].append(i.ratio_inventory_turnover)
            data_1[a].append(i.ratio_fixed_assets_turnover)
            data_1[a].append(i.ratio_tot_assets_turnover)
            data_1[a].append(i.ratio_net_assets)
            data_1[a].append(i.ratio_fixed_assets)
            a=a+1
    return jsonify(data_1)
