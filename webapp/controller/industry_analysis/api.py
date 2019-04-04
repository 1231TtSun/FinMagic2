from . import industry_analysis
from flask import request,jsonify
from webapp.models import *

@industry_analysis.route('api_get_date', methods=['GET'])
def api_get_date():
    result = bkqj_cndtqj.query.filter_by(industry_name='交通运输').all()
    date_list_all = []
    for i in result:
        date_list_all.append(i.date)
    date_list_all.sort(reverse=True)
    date_list = date_list_all[0:30]
    return jsonify(date_list)

# 资金流向全景获取今日交易资金量（按行业）
@industry_analysis.route('api_cndtqj_jyzjl_1', methods=('GET', 'POST'))
def api_cndtqj_jyzjl_1():
    date = request.values.get('date')
    index_name = request.values.get('index')
    result1 = bkqj_cndtqj.query.filter_by(date=date).all()
    data = {}
    data_1 = {}
    data_1['industry_name'] = []
    data_1[index_name] = []
    if index_name == 'transaction_capital':
        for i in result1:
            # data[i.industry_name] = int(i.transaction_capital/100000000)
            exec('data[i.industry_name] = int(i.' + index_name + ' / 100000000)')
    elif index_name == 'cur_market_value':
        for i in result1:
            exec('data[i.industry_name] = int(i.' + index_name + ' / 100000000000)')
    else:
        for i in result1:
            exec('data[i.industry_name] = round(i.' + index_name + ',1)')

    result = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        i = list(i)
        data_1['industry_name'].append(i[0])
        data_1[index_name].append(i[1])
    return jsonify(data_1)

# 资金流向全景获取近n日交易资金量（按行业）
@industry_analysis.route('api_cndtqj_jyzjl_n', methods=('GET', 'POST'))
def api_cndtqj_jyzjl_n():
    date = request.values.getlist('date[]')
    index_name = request.values.get('index')
    result_all = {}
    result_added = {}
    data_1 = {}
    data_1['industry_name'] = []
    data_1[index_name] = []
    for i in range(0, len(date)):
        if i == 0:
            result1 = bkqj_cndtqj.query.filter_by(date=date[i]).all()
            for a in result1:
                result_all[a.industry_name] = []
                exec('result_all[a.industry_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
        else:
            result1 = bkqj_cndtqj.query.filter_by(date=date[i]).all()
            for a in result1:
                exec('result_all[a.industry_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
    for i in result_all:
        sum = 0
        for a in result_all[i]:
            if a is None:
                a = 0
            sum += a
        if index_name == 'transaction_capital':
            result_added[i] = int(sum / 100000000)
        elif index_name == 'cur_market_value':
            result_added[i] = int(sum / 100000000000)
        else:
            result_added[i] = round(sum, 1)
    result = sorted(result_added.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        i = list(i)
        data_1['industry_name'].append(i[0])
        data_1[index_name].append(i[1])
    return jsonify(data_1)

# 资金流向全景交易资金变化率（按行业）
@industry_analysis.route('api_cndtqj_jyzjbhl', methods=('GET', 'POST'))
def api_cndtqj_jyzjbhl():
    date = request.values.getlist('date[]')
    index_name = request.values.get('index')
    result_all = {}
    result_bhl = {}
    data_1 = {}
    data_1['industry_name'] = []
    data_1[index_name] = []
    for i in range(0, len(date)):
        if i == 0:
            result1 = bkqj_cndtqj.query.filter_by(date=date[i]).all()
            for a in result1:
                result_all[a.industry_name] = []
                exec('result_all[a.industry_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
        else:
            result1 = bkqj_cndtqj.query.filter_by(date=date[i]).all()
            for a in result1:
                exec('result_all[a.industry_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
    for i in result_all:
        bhl = round((result_all[i][0] - result_all[i][1]) / result_all[i][1], 1)
        result_bhl[i] = bhl
    result = sorted(result_bhl.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        i = list(i)
        data_1['industry_name'].append(i[0])
        data_1[index_name].append(i[1])
    return jsonify(data_1)

# 资金流向表格获取30天资金走势、资金变化率、当日变化率（按行业）
@industry_analysis.route('api_tb_zjzs', methods=(['GET','POST']))
def api_tb_zjzs():
    td_date = request.values.get('date')
    index_name = request.values.get('index')
    result_all = {}
    result = bkqj_cndtqj.query.filter(bkqj_cndtqj.date <= td_date).all()
    for i in result:
        if index_name == 'transaction_capital':
            if result_all.__contains__(i.industry_name):
                exec("result_all[i.industry_name]['zjzs'].append(int(i." + index_name + "/100000000))")
                # result_all[i.industry_name]['zjzs'].append(int(i.transaction_capital/100000000))
            else:
                result_all[i.industry_name] = {}
                result_all[i.industry_name]['zjzs'] = []
                exec("result_all[i.industry_name]['zjzs'].append(int(i." + index_name + "/100000000))")
                # result_all[i.industry_name]['zjzs'].append(int(i.transaction_capital/100000000))
        elif index_name == 'cur_market_value':
            if result_all.__contains__(i.industry_name):
                exec("result_all[i.industry_name]['zjzs'].append(int(i." + index_name + "/100000000000))")
            else:
                result_all[i.industry_name] = {}
                result_all[i.industry_name]['zjzs'] = []
                exec("result_all[i.industry_name]['zjzs'].append(int(i." + index_name + "/100000000000))")
        else:
            if result_all.__contains__(i.industry_name):
                exec("result_all[i.industry_name]['zjzs'].append(i." + index_name + ")")
            else:
                result_all[i.industry_name] = {}
                result_all[i.industry_name]['zjzs'] = []
                exec("result_all[i.industry_name]['zjzs'].append(i." + index_name + ")")
    for i in result_all:
        result_all[i]['zjzs'] = result_all[i]['zjzs'][len(result_all[i]['zjzs']) - 30:len(result_all[i]['zjzs'])]
        result_all[i]['zjbhl'] = []
        # 当前为计算29天变化率
        for a in range(1, 30):
            if result_all[i]['zjzs'][a - 1] == 0:
                result_all[i]['zjbhl'].append(1)
            elif result_all[i]['zjzs'][a - 1] is None:
                result_all[i]['zjzs'][a - 1] = 0
                # result_all[i]['zjbhl'].append(1)
            elif result_all[i]['zjzs'][a] is None:
                result_all[i]['zjzs'][a] = 0
                result_all[i]['zjbhl'].append(0)
            else:
                result_all[i]['zjbhl'].append(
                    round((result_all[i]['zjzs'][a] - result_all[i]['zjzs'][a - 1]) / result_all[i]['zjzs'][a - 1], 2))
        result_all[i]['jrbhl'] = result_all[i]['zjbhl'][-1]
    result_sorted = sorted(result_all.items(), key=lambda x: x[1]['jrbhl'], reverse=True)
    # print(result_sorted[0][1]['jrbhl'])
    return jsonify(result_sorted)

# 资金流向全景获取今日交易资金量（按地域）
@industry_analysis.route('api_cndtqj_jyzjl_1_region', methods=('GET', 'POST'))
def api_cndtqj_jyzjl_1_region():
    date = request.values.get('date')
    index_name = request.values.get('index')
    result1 = bkqj_cndtqj_region.query.filter_by(date=date).all()
    data = {}
    data_1 = {}
    data_1['region_name'] = []
    data_1[index_name] = []
    if index_name == 'transaction_capital':
        for i in result1:
            # data[i.industry_name] = int(i.transaction_capital/100000000)
            exec('data[i.region_name] = int(i.' + index_name + ' / 100000000)')
    elif index_name == 'cur_market_value':
        for i in result1:
            exec('data[i.region_name] = int(i.' + index_name + ' / 100000000000)')
    else:
        for i in result1:
            exec('data[i.region_name] = round(i.' + index_name + ',1)')

    result = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        i = list(i)
        data_1['region_name'].append(i[0])
        data_1[index_name].append(i[1])
    return jsonify(data_1)

# 资金流向全景获取近n日交易资金量（按地域）
@industry_analysis.route('api_cndtqj_jyzjl_n_region', methods=('GET', 'POST'))
def api_cndtqj_jyzjl_n_region():
    date = request.values.getlist('date[]')
    index_name = request.values.get('index')
    result_all = {}
    result_added = {}
    data_1 = {}
    data_1['region_name'] = []
    data_1[index_name] = []
    for i in range(0, len(date)):
        if i == 0:
            result1 = bkqj_cndtqj_region.query.filter_by(date=date[i]).all()
            for a in result1:
                result_all[a.region_name] = []
                exec('result_all[a.region_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
        else:
            result1 = bkqj_cndtqj_region.query.filter_by(date=date[i]).all()
            for a in result1:
                exec('result_all[a.region_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
    for i in result_all:
        sum = 0
        for a in result_all[i]:
            if a is None:
                a = 0
            sum += a
        if index_name == 'transaction_capital':
            result_added[i] = int(sum / 100000000)
        elif index_name == 'cur_market_value':
            result_added[i] = int(sum / 100000000000)
        else:
            result_added[i] = round(sum, 1)
    result = sorted(result_added.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        i = list(i)
        data_1['region_name'].append(i[0])
        data_1[index_name].append(i[1])
    return jsonify(data_1)

# 资金流向全景交易资金变化率（按地域）
@industry_analysis.route('api_cndtqj_jyzjbhl_region', methods=('GET', 'POST'))
def api_cndtqj_jyzjbhl_region():
    date = request.values.getlist('date[]')
    index_name = request.values.get('index')
    result_all = {}
    result_bhl = {}
    data_1 = {}
    data_1['region_name'] = []
    data_1[index_name] = []
    for i in range(0, len(date)):
        if i == 0:
            result1 = bkqj_cndtqj_region.query.filter_by(date=date[i]).all()
            for a in result1:
                result_all[a.region_name] = []
                exec('result_all[a.region_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
        else:
            result1 = bkqj_cndtqj_region.query.filter_by(date=date[i]).all()
            for a in result1:
                exec('result_all[a.region_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
    for i in result_all:
        bhl = round((result_all[i][0] - result_all[i][1]) / result_all[i][1], 1)
        result_bhl[i] = bhl
    result = sorted(result_bhl.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        i = list(i)
        data_1['region_name'].append(i[0])
        data_1[index_name].append(i[1])
    return jsonify(data_1)

# 资金流向表格获取30天资金走势、资金变化率、当日变化率（按地域）
@industry_analysis.route('api_tb_zjzs_region', methods=(['GET','POST']))
def api_tb_zjzs_region():
    td_date = request.values.get('date')
    index_name = request.values.get('index')
    result_all = {}
    result = bkqj_cndtqj_region.query.filter(bkqj_cndtqj_region.date <= td_date).all()
    for i in result:
        if index_name == 'transaction_capital':
            if result_all.__contains__(i.region_name):
                exec("result_all[i.region_name]['zjzs'].append(int(i." + index_name + "/100000000))")
                # result_all[i.industry_name]['zjzs'].append(int(i.transaction_capital/100000000))
            else:
                result_all[i.region_name] = {}
                result_all[i.region_name]['zjzs'] = []
                exec("result_all[i.region_name]['zjzs'].append(int(i." + index_name + "/100000000))")
                # result_all[i.industry_name]['zjzs'].append(int(i.transaction_capital/100000000))
        elif index_name == 'cur_market_value':
            if result_all.__contains__(i.region_name):
                exec("result_all[i.region_name]['zjzs'].append(int(i." + index_name + "/100000000000))")
            else:
                result_all[i.region_name] = {}
                result_all[i.region_name]['zjzs'] = []
                exec("result_all[i.region_name]['zjzs'].append(int(i." + index_name + "/100000000000))")
        else:
            if result_all.__contains__(i.region_name):
                exec("result_all[i.region_name]['zjzs'].append(i." + index_name + ")")
            else:
                result_all[i.region_name] = {}
                result_all[i.region_name]['zjzs'] = []
                exec("result_all[i.region_name]['zjzs'].append(i." + index_name + ")")
    for i in result_all:
        result_all[i]['zjzs'] = result_all[i]['zjzs'][len(result_all[i]['zjzs']) - 30:len(result_all[i]['zjzs'])]
        result_all[i]['zjbhl'] = []
        # 当前为计算29天变化率
        for a in range(1, 30):
            if result_all[i]['zjzs'][a - 1] == 0:
                result_all[i]['zjbhl'].append(1)
            elif result_all[i]['zjzs'][a - 1] is None:
                result_all[i]['zjzs'][a - 1] = 0
                # result_all[i]['zjbhl'].append(1)
            elif result_all[i]['zjzs'][a] is None:
                result_all[i]['zjzs'][a] = 0
                result_all[i]['zjbhl'].append(0)
            else:
                result_all[i]['zjbhl'].append(
                    round((result_all[i]['zjzs'][a] - result_all[i]['zjzs'][a - 1]) / result_all[i]['zjzs'][a - 1], 2))
        result_all[i]['jrbhl'] = result_all[i]['zjbhl'][-1]
    result_sorted = sorted(result_all.items(), key=lambda x: x[1]['jrbhl'], reverse=True)
    return jsonify(result_sorted)

# 资金流向全景获取今日交易资金量（按概念）
@industry_analysis.route('api_cndtqj_jyzjl_1_conceptual', methods=('GET', 'POST'))
def api_cndtqj_jyzjl_1_conceptual():
    date = request.values.get('date')
    index_name = request.values.get('index')
    result1 = bkqj_cndtqj_conceptual.query.filter_by(date=date).all()
    data = {}
    data_1 = {}
    data_1['conceptual_name'] = []
    data_1[index_name] = []
    num = 0
    if index_name == 'transaction_capital':
        for i in result1:
            # data[i.industry_name] = int(i.transaction_capital/100000000)
            exec('data[i.conceptual_name] = int(i.' + index_name + ' / 100000000)')
    elif index_name == 'cur_market_value':
        for i in result1:
            exec('data[i.conceptual_name] = int(i.' + index_name + ' / 100000000000)')
    else:
        for i in result1:
            exec('data[i.conceptual_name] = round(i.' + index_name + ',1)')

    result = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        if num < 33:
            i = list(i)
            data_1['conceptual_name'].append(i[0])
            data_1[index_name].append(i[1])
            num += 1
    return jsonify(data_1)

# 资金流向全景获取近n日交易资金量（按概念）
@industry_analysis.route('api_cndtqj_jyzjl_n_conceptual', methods=('GET', 'POST'))
def api_cndtqj_jyzjl_n_conceptual():
    date = request.values.getlist('date[]')
    index_name = request.values.get('index')
    result_all = {}
    result_added = {}
    data_1 = {}
    data_1['conceptual_name'] = []
    data_1[index_name] = []
    num = 0
    for i in range(0, len(date)):
        if i == 0:
            result1 = bkqj_cndtqj_conceptual.query.filter_by(date=date[i]).all()
            for a in result1:
                result_all[a.conceptual_name] = []
                exec('result_all[a.conceptual_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
        else:
            result1 = bkqj_cndtqj_conceptual.query.filter_by(date=date[i]).all()
            for a in result1:
                exec('result_all[a.conceptual_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
    for i in result_all:
        sum = 0
        for a in result_all[i]:
            if a is None:
                a = 0
            sum += a
        if index_name == 'transaction_capital':
            result_added[i] = int(sum / 100000000)
        elif index_name == 'cur_market_value':
            result_added[i] = int(sum / 100000000000)
        else:
            result_added[i] = round(sum, 1)
    result = sorted(result_added.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        if num < 33:
            i = list(i)
            data_1['conceptual_name'].append(i[0])
            data_1[index_name].append(i[1])
            num += 1
    return jsonify(data_1)

# 资金流向全景交易资金变化率（按概念）
@industry_analysis.route('api_cndtqj_jyzjbhl_conceptual', methods=('GET', 'POST'))
def api_cndtqj_jyzjbhl_conceptual():
    date = request.values.getlist('date[]')
    index_name = request.values.get('index')
    result_all = {}
    result_bhl = {}
    data_1 = {}
    data_1['conceptual_name'] = []
    data_1[index_name] = []
    num = 0
    for i in range(0, len(date)):
        if i == 0:
            result1 = bkqj_cndtqj_conceptual.query.filter_by(date=date[i]).all()
            for a in result1:
                result_all[a.conceptual_name] = []
                exec('result_all[a.conceptual_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
        else:
            result1 = bkqj_cndtqj_conceptual.query.filter_by(date=date[i]).all()
            for a in result1:
                exec('result_all[a.conceptual_name].append(a.' + index_name + ')')
                # result_all[a.industry_name].append(a.transaction_capital)
    for i in result_all:
        bhl = round((result_all[i][0] - result_all[i][1]) / result_all[i][1], 1)
        result_bhl[i] = bhl
    result = sorted(result_bhl.items(), key=lambda x: x[1], reverse=True)
    for i in result:
        if num < 33:
            i = list(i)
            data_1['conceptual_name'].append(i[0])
            data_1[index_name].append(i[1])
            num += 1
    return jsonify(data_1)

# 资金流向表格获取30天资金走势、资金变化率、当日变化率（按概念）
@industry_analysis.route('api_tb_zjzs_conceptual', methods=(['GET','POST']))
def api_tb_zjzs_conceptual():
    td_date = request.values.get('date')
    index_name = request.values.get('index')
    result_all = {}
    num = 0
    result = bkqj_cndtqj_conceptual.query.filter(bkqj_cndtqj_conceptual.date <= td_date).all()
    for i in result:
        if index_name == 'transaction_capital':
            if result_all.__contains__(i.conceptual_name):
                exec("result_all[i.conceptual_name]['zjzs'].append(int(i." + index_name + "/100000000))")
                # result_all[i.industry_name]['zjzs'].append(int(i.transaction_capital/100000000))
            else:
                result_all[i.conceptual_name] = {}
                result_all[i.conceptual_name]['zjzs'] = []
                exec("result_all[i.conceptual_name]['zjzs'].append(int(i." + index_name + "/100000000))")
                # result_all[i.industry_name]['zjzs'].append(int(i.transaction_capital/100000000))
        elif index_name == 'cur_market_value':
            if result_all.__contains__(i.conceptual_name):
                exec("result_all[i.conceptual_name]['zjzs'].append(int(i." + index_name + "/100000000000))")
            else:
                result_all[i.conceptual_name] = {}
                result_all[i.conceptual_name]['zjzs'] = []
                exec("result_all[i.conceptual_name]['zjzs'].append(int(i." + index_name + "/100000000000))")
        else:
            if result_all.__contains__(i.conceptual_name):
                exec("result_all[i.conceptual_name]['zjzs'].append(i." + index_name + ")")
            else:
                result_all[i.conceptual_name] = {}
                result_all[i.conceptual_name]['zjzs'] = []
                exec("result_all[i.conceptual_name]['zjzs'].append(i." + index_name + ")")

    for i in result_all:
        # if num < 30:
        result_all[i]['zjzs'] = result_all[i]['zjzs'][len(result_all[i]['zjzs']) - 30:len(result_all[i]['zjzs'])]
        result_all[i]['zjbhl'] = []
        # 当前为计算29天变化率
        for a in range(1, 30):
            if result_all[i]['zjzs'][a - 1] == 0:
                result_all[i]['zjbhl'].append(1)
            elif result_all[i]['zjzs'][a - 1] is None:
                result_all[i]['zjzs'][a - 1] = 0
                # result_all[i]['zjbhl'].append(1)
            elif result_all[i]['zjzs'][a] is None:
                result_all[i]['zjzs'][a] = 0
                result_all[i]['zjbhl'].append(0)
            else:
                result_all[i]['zjbhl'].append(
                    round((result_all[i]['zjzs'][a] - result_all[i]['zjzs'][a - 1]) / result_all[i]['zjzs'][a - 1], 2))
        result_all[i]['jrbhl'] = result_all[i]['zjbhl'][-1]
        num += 1
    result_sorted = sorted(result_all.items(), key=lambda x: x[1]['jrbhl'], reverse=True)
    # print(result_sorted[0][1]['jrbhl'])
    return jsonify(result_sorted)

# 板块全景指标比较获取全部行业
@industry_analysis.route('api_get_all_industry', methods=(['GET','POST']))
def api_get_all_industry():
    session = DBSession()
    user = session.query(distinct(qjzn.industry2)).all()
    result = []
    for i in user:
        result.append(i[0])
    return jsonify(result)

# 根据行业获取股票及其财务信息
@industry_analysis.route('api_get_industry_stock_data', methods=(['GET','POST']))
def api_get_industry_stock_data():
    industry = request.values.get('industry')
    session = DBSession()
    stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.industry2 == industry).all()
    stock_code_list = []
    for i in stock_code:
        stock_code_list.append(i[0]);
    result = {}
    result_sj = session.query(jccwsj.ts_code, jccwsj.sec_name, jccwsj.eps_basic_is, jccwsj.net_profit_is,
                              jccwsj.tot_assets, jccwsj.tot_liab).filter(jccwsj.the_date == "2018-09-30").all()
    result_zb = session.query(jccwzb.ts_code, jccwzb.pro_margin_main_business, jccwzb.rate_return_on_equity,
                              jccwzb.ratio_current,
                              jccwzb.ratio_asset_liability, jccwzb.growth_rate_net_profit,
                              jccwzb.growth_rate_net_assets,
                              jccwzb.ratio_inventory_turnover, jccwzb.ratio_tot_assets_turnover).filter(
        jccwzb.date == "20181101").all()
    for i in result_zb:
        if i[0] in stock_code_list:
            result[i[0]] = {}
            result[i[0]]['pro_margin_main_business'] = i[1]
            result[i[0]]['rate_return_on_equity'] = i[2]
            result[i[0]]['ratio_current'] = i[3]
            result[i[0]]['ratio_asset_liability'] = i[4]
            result[i[0]]['growth_rate_net_profit'] = i[5]
            result[i[0]]['growth_rate_net_assets'] = i[6]
            result[i[0]]['ratio_inventory_turnover'] = i[7]
            result[i[0]]['ratio_tot_assets_turnover'] = i[8]
    for i in result_sj:
        if i[0] in result.keys():
            result[i[0]]['sec_name'] = i[1]
            result[i[0]]['eps_basic_is'] = i[2]
            if result[i[0]]['eps_basic_is'] > 0:
                result[i[0]]['color'] = 'red'
            elif result[i[0]]['eps_basic_is'] == 0:
                result[i[0]]['color'] = 'black'
            else:
                result[i[0]]['color'] = 'green'
            result[i[0]]['net_profit_is'] = round(i[3] / 100000000, 2)
            result[i[0]]['tot_assets'] = round(i[4] / 100000000, 2)
            result[i[0]]['tot_liab'] = round(i[5] / 100000000, 2)
            result[i[0]]['score'] = '-'
    return jsonify(result)

# 板块全景指标比较获取全部地域
@industry_analysis.route('api_get_all_region', methods=(['GET','POST']))
def api_get_all_region():
    session = DBSession()
    user = session.query(distinct(region.region_name)).all()
    result = []
    for i in user:
        result.append(i[0])
    return jsonify(result)

# 根据地域获取相应股票及其财务信息
@industry_analysis.route('api_get_region_stock_data', methods=(['GET','POST']))
def api_get_region_stock_data():
    region_clicked = request.values.get('region')
    session = DBSession()
    region_dict = {
        "上海": ['province', '上海'],
        "云南": ['province', '云南省'],
        "内蒙古": ['province', '内蒙古自治区'],
        "北京": ['province', '北京'],
        "吉林": ['province', '吉林省'],
        "宁夏": ['province', '宁夏回族自治区'],
        "安徽": ['province', '安徽省'],
        "山东": ['province', '山东省'],
        "山西": ['province', '山西省'],
        "广东": ['province', '广东省'],
        "广州": ['city', '广州市'],
        "广西": ['province', '广西壮族自治区'],
        "新疆": ['province', '新疆维吾尔自治区'],
        "江苏": ['province', '江苏省'],
        "江西": ['province', '江西省'],
        "河北": ['province', '河北省'],
        "河南": ['province', '河南省'],
        "浙江": ['province', '浙江省'],
        "深圳": ['city', '深圳市'],
        "海南": ['province', '海南省'],
        "湖北": ['province', '湖北省'],
        "湖南": ['province', '湖南省'],
        "甘肃": ['province', '甘肃省'],
        "福建": ['province', '福建省'],
        "西藏": ['province', '西藏自治区'],
        "贵州": ['province', '贵州省'],
        "辽宁": ['province', '辽宁省'],
        "重庆": ['province', '重庆'],
        "陕西": ['province', '陕西省'],
        "青海": ['province', '青海省'],
        "黑龙江": ['province', '黑龙江省']
    }
    type = region_dict[region_clicked][0]
    region_1 = region_dict[region_clicked][1]
    if type == 'city':
        stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.city == region_1).all()
    else:
        stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.province == region_1).all()
    stock_code_list = []
    for i in stock_code:
        stock_code_list.append(i[0]);
    result = {}
    result_sj = session.query(jccwsj.ts_code, jccwsj.sec_name, jccwsj.eps_basic_is, jccwsj.net_profit_is,
                              jccwsj.tot_assets, jccwsj.tot_liab).filter(jccwsj.the_date == "2018-09-30").all()
    result_zb = session.query(jccwzb.ts_code, jccwzb.pro_margin_main_business, jccwzb.rate_return_on_equity,
                              jccwzb.ratio_current,
                              jccwzb.ratio_asset_liability, jccwzb.growth_rate_net_profit,
                              jccwzb.growth_rate_net_assets,
                              jccwzb.ratio_inventory_turnover, jccwzb.ratio_tot_assets_turnover).filter(
        jccwzb.date == "20181101").all()
    for i in result_zb:
        if i[0] in stock_code_list:
            result[i[0]] = {}
            result[i[0]]['pro_margin_main_business'] = i[1]
            result[i[0]]['rate_return_on_equity'] = i[2]
            result[i[0]]['ratio_current'] = i[3]
            result[i[0]]['ratio_asset_liability'] = i[4]
            result[i[0]]['growth_rate_net_profit'] = i[5]
            result[i[0]]['growth_rate_net_assets'] = i[6]
            result[i[0]]['ratio_inventory_turnover'] = i[7]
            result[i[0]]['ratio_tot_assets_turnover'] = i[8]
    for i in result_sj:
        if i[0] in result.keys():
            result[i[0]]['sec_name'] = i[1]
            result[i[0]]['eps_basic_is'] = i[2]
            if result[i[0]]['eps_basic_is'] > 0:
                result[i[0]]['color'] = 'red'
            elif result[i[0]]['eps_basic_is'] == 0:
                result[i[0]]['color'] = 'black'
            else:
                result[i[0]]['color'] = 'green'
            result[i[0]]['net_profit_is'] = round(i[3] / 100000000, 2)
            result[i[0]]['tot_assets'] = round(i[4] / 100000000, 2)
            result[i[0]]['tot_liab'] = round(i[5] / 100000000, 2)
            result[i[0]]['score'] = '-'
    return jsonify(result)

# 板块全景指标比较获取全部概念板块
@industry_analysis.route('api_get_all_concept', methods=(['GET','POST']))
def api_get_all_concept():
    session = DBSession()
    concept = session.query(distinct(qjzn.concept)).all()
    concept_all = []
    num = 0
    for i in concept:  # 对每只板块的股票进行循环
        str = ""
        for a in i[0]:  # 对股票所属板块的每个字进行循环
            if a == ";":  # 如果遇到分号
                if str in concept_all:
                    str = ""
                else:
                    concept_all.append(str)
                    str = ""
            else:
                str = str + a
    return jsonify(concept_all)

# 根据概念板块获取相应股票及其财务信息
@industry_analysis.route('api_get_concept_stock_data', methods=(['GET','POST']))
def api_get_concept_stock_data():
    concept_clicked = request.values.get('concept')
    session = DBSession()
    stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.concept.like("%" + concept_clicked + "%")).all()
    stock_code_list = []
    for i in stock_code:
        stock_code_list.append(i[0])
    result = {}
    result_sj = session.query(jccwsj.ts_code, jccwsj.sec_name, jccwsj.eps_basic_is, jccwsj.net_profit_is,
                              jccwsj.tot_assets, jccwsj.tot_liab).filter(jccwsj.the_date == "2018-09-30").all()
    result_zb = session.query(jccwzb.ts_code, jccwzb.pro_margin_main_business, jccwzb.rate_return_on_equity,
                              jccwzb.ratio_current,
                              jccwzb.ratio_asset_liability, jccwzb.growth_rate_net_profit,
                              jccwzb.growth_rate_net_assets,
                              jccwzb.ratio_inventory_turnover, jccwzb.ratio_tot_assets_turnover).filter(
        jccwzb.date == "20181101").all()
    for i in result_zb:
        if i[0] in stock_code_list:
            result[i[0]] = {}
            result[i[0]]['pro_margin_main_business'] = i[1]
            result[i[0]]['rate_return_on_equity'] = i[2]
            result[i[0]]['ratio_current'] = i[3]
            result[i[0]]['ratio_asset_liability'] = i[4]
            result[i[0]]['growth_rate_net_profit'] = i[5]
            result[i[0]]['growth_rate_net_assets'] = i[6]
            result[i[0]]['ratio_inventory_turnover'] = i[7]
            result[i[0]]['ratio_tot_assets_turnover'] = i[8]
    for i in result_sj:
        if i[0] in result.keys():
            result[i[0]]['sec_name'] = i[1]
            result[i[0]]['eps_basic_is'] = i[2]
            if result[i[0]]['eps_basic_is'] > 0:
                result[i[0]]['color'] = 'red'
            elif result[i[0]]['eps_basic_is'] == 0:
                result[i[0]]['color'] = 'black'
            else:
                result[i[0]]['color'] = 'green'
            result[i[0]]['net_profit_is'] = round(i[3] / 100000000, 2)
            result[i[0]]['tot_assets'] = round(i[4] / 100000000, 2)
            result[i[0]]['tot_liab'] = round(i[5] / 100000000, 2)
            result[i[0]]['score'] = '-'
    return jsonify(result)

# 根据行业获取股票及其行情数据
@industry_analysis.route('api_get_industry_stock_market_data', methods=(['GET','POST']))
def api_get_industry_stock_market_data():
    industry = request.values.get('industry')
    session = DBSession()
    stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.industry2 == industry).all()
    stock_code_list = []
    for i in stock_code:
        stock_code_list.append(i[0])
    result = {}
    result_sj = session.query(jcrxsj.ts_code, jcrxsj.ts_name, jcrxsj.pct_change,
                              jcrxsj.open, jcrxsj.high, jcrxsj.low, jcrxsj.pre_close, jcrxsj.turnover_rate, jcrxsj.vol,
                              jcrxsj.amount, jcrxsj.cir_value, jcrxsj.pe_ttm, jcrxsj.pb).filter(
        jcrxsj.trade_date == "2018-11-30").all()
    for i in result_sj:
        if i[0] in stock_code_list:
            result[i[0]] = {}
            result[i[0]]['ts_name'] = i[1]
            result[i[0]]['pct_change'] = i[2]
            result[i[0]]['open'] = i[3]
            result[i[0]]['high'] = i[4]
            result[i[0]]['low'] = i[5]
            result[i[0]]['pre_close'] = i[6]
            result[i[0]]['turnover_rate'] = i[7]
            result[i[0]]['vol'] = i[8]
            if i[9] is None:
                result[i[0]]['amount'] = 0
            else:
                result[i[0]]['amount'] = round(i[9] / 100000000, 2)
            if result[i[0]]['pct_change'] is None:
                result[i[0]]['color'] = 'black'
            elif result[i[0]]['pct_change'] > 0:
                result[i[0]]['color'] = 'red'
            elif result[i[0]]['pct_change'] == 0:
                result[i[0]]['color'] = 'black'
            else:
                result[i[0]]['color'] = 'green'
            if i[10] is None:
                result[i[0]]['cir_value'] = 0
            else:
                result[i[0]]['cir_value'] = round(i[10] / 100000000, 2)
            result[i[0]]['pe_ttm'] = i[11]
            result[i[0]]['pb'] = i[12]
            result[i[0]]['score'] = '-'
            result[i[0]]['current'] = '-'
    return jsonify(result)

# 根据地域获取相应股票及其数据
@industry_analysis.route('api_get_region_stock_market_data', methods=(['GET','POST']))
def api_get_region_stock_market_data():
    region_clicked = request.values.get('region')
    session = DBSession()
    region_dict = {
        "上海": ['province', '上海'],
        "云南": ['province', '云南省'],
        "内蒙古": ['province', '内蒙古自治区'],
        "北京": ['province', '北京'],
        "吉林": ['province', '吉林省'],
        "宁夏": ['province', '宁夏回族自治区'],
        "安徽": ['province', '安徽省'],
        "山东": ['province', '山东省'],
        "山西": ['province', '山西省'],
        "广东": ['province', '广东省'],
        "广州": ['city', '广州市'],
        "广西": ['province', '广西壮族自治区'],
        "新疆": ['province', '新疆维吾尔自治区'],
        "江苏": ['province', '江苏省'],
        "江西": ['province', '江西省'],
        "河北": ['province', '河北省'],
        "河南": ['province', '河南省'],
        "浙江": ['province', '浙江省'],
        "深圳": ['city', '深圳市'],
        "海南": ['province', '海南省'],
        "湖北": ['province', '湖北省'],
        "湖南": ['province', '湖南省'],
        "甘肃": ['province', '甘肃省'],
        "福建": ['province', '福建省'],
        "西藏": ['province', '西藏自治区'],
        "贵州": ['province', '贵州省'],
        "辽宁": ['province', '辽宁省'],
        "重庆": ['province', '重庆'],
        "陕西": ['province', '陕西省'],
        "青海": ['province', '青海省'],
        "黑龙江": ['province', '黑龙江省']
    }
    type = region_dict[region_clicked][0]
    region_1 = region_dict[region_clicked][1]
    if type == 'city':
        stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.city == region_1).all()
    else:
        stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.province == region_1).all()
    stock_code_list = []
    for i in stock_code:
        stock_code_list.append(i[0])
    result = {}
    result_sj = session.query(jcrxsj.ts_code, jcrxsj.ts_name, jcrxsj.pct_change,
                              jcrxsj.open, jcrxsj.high, jcrxsj.low, jcrxsj.pre_close, jcrxsj.turnover_rate, jcrxsj.vol,
                              jcrxsj.amount, jcrxsj.cir_value, jcrxsj.pe_ttm, jcrxsj.pb).filter(
        jcrxsj.trade_date == "2018-11-30").all()
    for i in result_sj:
        if i[0] in stock_code_list:
            result[i[0]] = {}
            result[i[0]]['ts_name'] = i[1]
            result[i[0]]['pct_change'] = i[2]
            result[i[0]]['open'] = i[3]
            result[i[0]]['high'] = i[4]
            result[i[0]]['low'] = i[5]
            result[i[0]]['pre_close'] = i[6]
            result[i[0]]['turnover_rate'] = i[7]
            result[i[0]]['vol'] = i[8]
            if i[9] is None:
                result[i[0]]['amount'] = 0
            else:
                result[i[0]]['amount'] = round(i[9] / 100000000, 2)
            if result[i[0]]['pct_change'] is None:
                result[i[0]]['color'] = 'black'
            elif result[i[0]]['pct_change'] > 0:
                result[i[0]]['color'] = 'red'
            elif result[i[0]]['pct_change'] == 0:
                result[i[0]]['color'] = 'black'
            else:
                result[i[0]]['color'] = 'green'
            if i[10] is None:
                result[i[0]]['cir_value'] = 0
            else:
                result[i[0]]['cir_value'] = round(i[10] / 100000000, 2)
            result[i[0]]['pe_ttm'] = i[11]
            result[i[0]]['pb'] = i[12]
            result[i[0]]['score'] = '-'
            result[i[0]]['current'] = '-'
    return jsonify(result)

# 根据概念板块获取相应股票及其数据
@industry_analysis.route('api_get_concept_stock_market_data', methods=(['GET','POST']))
def api_get_concept_stock_market_data():
    concept_clicked = request.values.get('concept')
    session = DBSession()
    stock_code = session.query(distinct(qjzn.stock_code)).filter(qjzn.concept.like("%" + concept_clicked + "%")).all()
    stock_code_list = []
    for i in stock_code:
        stock_code_list.append(i[0])
    result = {}
    result_sj = session.query(jcrxsj.ts_code, jcrxsj.ts_name, jcrxsj.pct_change,
                              jcrxsj.open, jcrxsj.high, jcrxsj.low, jcrxsj.pre_close, jcrxsj.turnover_rate, jcrxsj.vol,
                              jcrxsj.amount, jcrxsj.cir_value, jcrxsj.pe_ttm, jcrxsj.pb).filter(
        jcrxsj.trade_date == "2018-11-30").all()
    for i in result_sj:
        if i[0] in stock_code_list:
            result[i[0]] = {}
            result[i[0]]['ts_name'] = i[1]
            result[i[0]]['pct_change'] = i[2]
            result[i[0]]['open'] = i[3]
            result[i[0]]['high'] = i[4]
            result[i[0]]['low'] = i[5]
            result[i[0]]['pre_close'] = i[6]
            result[i[0]]['turnover_rate'] = i[7]
            result[i[0]]['vol'] = i[8]
            if i[9] is None:
                result[i[0]]['amount'] = 0
            else:
                result[i[0]]['amount'] = round(i[9] / 100000000, 2)
            if result[i[0]]['pct_change'] is None:
                result[i[0]]['color'] = 'black'
            elif result[i[0]]['pct_change'] > 0:
                result[i[0]]['color'] = 'red'
            elif result[i[0]]['pct_change'] == 0:
                result[i[0]]['color'] = 'black'
            else:
                result[i[0]]['color'] = 'green'
            if i[10] is None:
                result[i[0]]['cir_value'] = 0
            else:
                result[i[0]]['cir_value'] = round(i[10] / 100000000, 2)
            result[i[0]]['pe_ttm'] = i[11]
            result[i[0]]['pb'] = i[12]
            result[i[0]]['score'] = '-'
            result[i[0]]['current'] = '-'
    return jsonify(result)

# 基础数据获取公司概况
@industry_analysis.route('api_get_stock_jcsj_gsgk', methods=(['GET','POST']))
def api_get_stock_jcsj_gsgk():
    stock = request.values.get('stock')
    session = DBSession()
    result = session.query(jcsj_gsgk.full_name, jcsj_gsgk.website, jcsj_gsgk.eng_name, jcsj_gsgk.short_name,
                           jcsj_gsgk.address, jcsj_gsgk.legal_representative, jcsj_gsgk.boardchairmen,
                           jcsj_gsgk.regist_captial, jcsj_gsgk.industry, jcsj_gsgk.phone, jcsj_gsgk.fax,
                           jcsj_gsgk.raise_date, jcsj_gsgk.exch_date, jcsj_gsgk.pub_num, jcsj_gsgk.pub_style,
                           jcsj_gsgk.pub_price, jcsj_gsgk.pub_ttm, jcsj_gsgk.industry_analysis_underwriter, jcsj_gsgk.exch_sponsors,
                           jcsj_gsgk.sponsor_agency).filter(jcsj_gsgk.ts_code == stock).all()
    underwriter = result[0][17]
    industry_analysis_underwritter = ""
    for i in underwriter:
        if i != ',':
            industry_analysis_underwritter += i
        else:
            break
    to_underwritter = session.query(jcsj_gsgk.ts_code,jcsj_gsgk.short_name).filter(jcsj_gsgk.industry_analysis_underwriter.like("%" + industry_analysis_underwritter + "%")).all()
    to_underwritter_list = []
    for i in to_underwritter:
        to_underwritter_list.append("● "+i[1]+"("+i[0]+")")
    result_all ={}
    result_all['full_name'] = result[0][0]
    result_all['website'] = result[0][1]
    result_all['eng_name'] = result[0][2]
    result_all['short_name'] = result[0][3]
    result_all['address'] = result[0][4]
    result_all['legal_representative'] = result[0][5]
    result_all['boardchairmen'] = result[0][6]
    result_all['regist_captial'] = result[0][7]
    result_all['industry'] = result[0][8]
    result_all['phone'] = result[0][9]
    result_all['fax'] = result[0][10]
    result_all['raise_date'] = result[0][11]
    result_all['exch_date'] = result[0][12]
    result_all['pub_num'] = result[0][13]/10000
    result_all['pub_style'] = result[0][14]
    result_all['pub_price'] = result[0][15]
    result_all['pub_ttm'] = result[0][16]
    result_all['industry_analysis_underwriter'] = industry_analysis_underwritter
    result_all['exch_sponsors'] = result[0][18]
    result_all['sponsor_agency'] = result[0][19]
    result_all['to_underwriter'] = to_underwritter_list
    result_all['to_underwriter_num'] = len(to_underwritter_list)
    return jsonify(result_all)

# 基础数据获取发行筹资
@industry_analysis.route('api_get_stock_jcsj_fxcz', methods=(['GET','POST']))
def api_get_stock_jcsj_fxcz():
    stock = request.values.get('stock')
    session = DBSession()
    result = session.query(jcsj_fxcz.pub_type, jcsj_fxcz.pub_date, jcsj_fxcz.pub_character, jcsj_fxcz.pub_stock_type,
                           jcsj_fxcz.pub_style, jcsj_fxcz.pub_stock_num, jcsj_fxcz.pub_price_cns,
                           jcsj_fxcz.pub_price_fore, jcsj_fxcz.act_fund, jcsj_fxcz.act_cost, jcsj_fxcz.pub_ttm,
                           jcsj_fxcz.lot_rate_oniline_pricing, jcsj_fxcz.bid_rate_sec_distribution).filter(jcsj_fxcz.ts_code == stock).all()
    return jsonify(result)

# 基础数据获取分红配股_分红
@industry_analysis.route('api_get_stock_jcsj_fh', methods=(['GET','POST']))
def api_get_stock_jcsj_fh():
    stock = request.values.get('stock')
    session = DBSession()
    result = session.query(jcsj_fhpg.bonus_year, jcsj_fhpg.bonus_plan, jcsj_fhpg.date_equity_regist, jcsj_fhpg.date_exclusion,
                           jcsj_fhpg.date_bonus_shares).filter(jcsj_fhpg.ts_code == stock).all()
    result_all={}
    result_all['bonus_year'] = []
    result_all['bonus_plan'] = []
    result_all['date_equity_regist'] = []
    result_all['date_exclusion'] = []
    result_all['date_bonus_shares'] = []
    result_all['index'] = []
    num = 1
    for i in result:
        result_all['bonus_year'].append(i[0].strftime('%Y')+"年度")
        if i[1] is None:
            result_all['bonus_plan'].append('-')
        else:
            result_all['bonus_plan'].append(i[1])
        if i[2] == '0000-00-00':
            result_all['date_equity_regist'].append('-')
        else:
            result_all['date_equity_regist'].append(i[2].strftime('%Y-%m-%d'))
        if i[3] == '0000-00-00':
            result_all['date_exclusion'].append('-')
        else:
            result_all['date_exclusion'].append(i[3].strftime('%Y-%m-%d'))
        if i[4] == '0000-00-00':
            result_all['date_bonus_shares'].append('-')
        else:
            result_all['date_bonus_shares'].append(i[4].strftime('%Y-%m-%d'))
        result_all['index'].append(num)
        num +=1
    return jsonify(result_all)

# 基础数据获取十大股东
@industry_analysis.route('api_get_stock_sdgd', methods=(['GET','POST']))
def api_get_stock_sdgd():
    stock = request.values.get('stock')
    session = DBSession()
    result = session.query(jcsj_sdgd.date, jcsj_sdgd.name, jcsj_sdgd.num, jcsj_sdgd.ratio,
                           jcsj_sdgd.type).filter(jcsj_sdgd.ts_code == stock).all()
    result_all = {}
    name_list = []
    for i in result:
        date = i[0].strftime('%Y-%m-%d')
        if date in result_all.keys():
            result_all[date]['name'].append(i[1])
            result_all[date]['num'].append(i[2])
            result_all[date]['ratio'].append(i[3])
            result_all[date]['type'].append(i[4])
        else:
            result_all[date]={}
            result_all[date]['name']=[]
            result_all[date]['num']=[]
            result_all[date]['ratio']=[]
            result_all[date]['type']=[]
            result_all[date]['name'].append(i[1])
            result_all[date]['num'].append(i[2])
            result_all[date]['ratio'].append(i[3])
            result_all[date]['type'].append(i[4])
        if i[1] not in name_list:
            name_list.append(i[1])
    result_all['tqdgd'] = {}
    for i in name_list:
        # 获取同期大股东的其他股票代码
        tqdgd = session.query(distinct(jcsj_sdgd.ts_code)).filter(jcsj_sdgd.name == i,jcsj_sdgd.ts_code != stock).all()
        if tqdgd != []:
            result_all['tqdgd'][i]=[]
            for a in tqdgd[0]:
                # 获取其他同期大股东股票代码的名称
                sec_name = session.query(jcsj_gsgk.short_name).filter(jcsj_gsgk.ts_code == a).all()
                print(sec_name[0][0])
                result_all['tqdgd'][i].append("● " + sec_name[0][0] + "(" + a + ")")
    return jsonify(result_all)
