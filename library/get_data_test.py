import time
from sqlalchemy import create_engine, VARCHAR
import tushare as ts
import pandas as pd
from xml.etree import ElementTree as ET


def get_abbreviation(string):
    from pypinyin import pinyin, Style
    pinyin_list = pinyin(string, style=Style.FIRST_LETTER)
    letter_list = []
    for char in pinyin_list:
        letter_list.append(char[0].upper())
    return ''.join(letter_list)


def update_stock_basic():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    pro = ts.pro_api()
    data = pro.stock_basic(
        fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    abbreviation_list = data.apply(lambda x: get_abbreviation(x['name']), axis=1)
    data['abbreviation'] = abbreviation_list
    pd.io.sql.to_sql(data, 'stock_basic', con=connect, schema='gupiaowajue2', if_exists='append', index=False)
    connect.dispose()


def update_market_calendar():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    pro = ts.pro_api()
    data = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')
    pd.io.sql.to_sql(data, 'market_calendar', con=connect, schema='gupiaowajue2', if_exists='append', index=False)
    connect.dispose()


def stock_daily_basic():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    pro = ts.pro_api()
    data = pro.daily_basic(ts_code='000001.SZ', start_date='20181201', end_date='20181231',
                           fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')
    pd.io.sql.to_sql(data, 'stock_daily_basic', con=connect, schema='gupiaowajue2', if_exists='append', index=False)
    connect.dispose()


def update_stock_industry_csrc_table():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    first_level_i = []
    first_level_n = []
    first_level_e = []
    second_level_i = []
    second_level_n = []
    second_level_e = []
    second_level_b = []
    tree = ET.parse('SysGrp.xml')
    root = tree.getroot()
    for x in root[0][1]:
        first_level_i.append(x.get('i'))
        first_level_n.append(x.get('n'))
        first_level_e.append(x.get('e'))
        for y in x:
            second_level_i.append(y.get('i'))
            second_level_n.append(y.get('n'))
            second_level_e.append(y.get('e'))
            second_level_b.append(x.get('i'))
    first_level_df = pd.DataFrame()
    second_level_df = pd.DataFrame()
    first_level_df['industry_csrc_1_code'] = first_level_i
    first_level_df['industry_csrc_1_name'] = first_level_n
    first_level_df['industry_csrc_1_enname'] = first_level_e
    second_level_df['industry_csrc_2_code'] = second_level_i
    second_level_df['industry_csrc_2_name'] = second_level_n
    second_level_df['industry_csrc_2_enname'] = second_level_e
    second_level_df['belong_to'] = second_level_b
    pd.io.sql.to_sql(first_level_df, 'stock_industry_csrc_1', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    pd.io.sql.to_sql(second_level_df, 'stock_industry_csrc_2', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    connect.dispose()


def update_stock_industry_sw_table():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    first_level_i = []
    first_level_n = []
    first_level_e = []
    second_level_i = []
    second_level_n = []
    second_level_e = []
    second_level_b = []
    third_level_i = []
    third_level_n = []
    third_level_e = []
    third_level_b = []
    tree = ET.parse('SysGrp.xml')
    root = tree.getroot()
    for x in root[0][3]:
        first_level_i.append(x.get('i'))
        first_level_n.append(x.get('n'))
        first_level_e.append(x.get('e'))
        for y in x:
            second_level_i.append(y.get('i'))
            second_level_n.append(y.get('n'))
            second_level_e.append(y.get('e'))
            second_level_b.append(x.get('i'))
            for z in y:
                third_level_i.append(z.get('i'))
                third_level_n.append(z.get('n'))
                third_level_e.append(z.get('e'))
                third_level_b.append(y.get('i'))
    first_level_df = pd.DataFrame()
    second_level_df = pd.DataFrame()
    third_level_df = pd.DataFrame()
    first_level_df['industry_sw_1_code'] = first_level_i
    first_level_df['industry_sw_1_name'] = first_level_n
    first_level_df['industry_sw_1_enname'] = first_level_e
    second_level_df['industry_sw_2_code'] = second_level_i
    second_level_df['industry_sw_2_name'] = second_level_n
    second_level_df['industry_sw_2_enname'] = second_level_e
    second_level_df['belong_to'] = second_level_b
    third_level_df['industry_sw_3_code'] = third_level_i
    third_level_df['industry_sw_3_name'] = third_level_n
    third_level_df['industry_sw_3_enname'] = third_level_e
    third_level_df['belong_to'] = third_level_b
    pd.io.sql.to_sql(first_level_df, 'stock_industry_sw_1', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    pd.io.sql.to_sql(second_level_df, 'stock_industry_sw_2', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    pd.io.sql.to_sql(third_level_df, 'stock_industry_sw_3', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    connect.dispose()


def update_stock_concept_table():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    concept_i = []
    concept_n = []
    concept_e = []
    tree = ET.parse('SysGrp.xml')
    root = tree.getroot()
    for x in root[0][14][1]:
        concept_i.append(x.get('i'))
        concept_n.append(x.get('n'))
        concept_e.append(x.get('e'))
    concept_df = pd.DataFrame()
    concept_df['concept_code'] = concept_i
    concept_df['concept_name'] = concept_n
    concept_df['concept_enname'] = concept_e
    concept_df['src'] = 'wind'
    pd.io.sql.to_sql(concept_df, 'stock_concept_list', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    pro = ts.pro_api()
    ts_data = pro.concept()
    ts_data.rename(columns={'code': 'concept_code', 'name': 'concept_name'}, inplace=True)
    pd.io.sql.to_sql(ts_data, 'stock_concept_list', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    concept_detail_concept_code = []
    concept_detail_ts_code = []
    concept_detail_name = []
    concept_detail_df = pd.DataFrame()
    from WindPy import w
    w.start()
    print("开始获取wind数据")
    for i in concept_i:
        data = w.wset('sectorconstituent', 'date=2019-03-01;sectorid=' + i)
        if data.Data == []:
            pass
        else:
            concept_detail_concept_code.extend([i] * len(data.Codes))
            concept_detail_ts_code.extend(data.Data[1])
            concept_detail_name.extend(data.Data[2])
    concept_detail_df['concept_code'] = concept_detail_concept_code
    concept_detail_df['ts_code'] = concept_detail_ts_code
    concept_detail_df['name'] = concept_detail_name
    concept_detail_df['src'] = 'wind'
    pd.io.sql.to_sql(concept_detail_df, 'stock_concept_detail', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    print("完成，开始获取tushare数据")
    for i in ts_data['concept_code'].tolist():
        data = pro.concept_detail(id=i, fields='id,ts_code,name,in_date,out_date')
        if data.empty:
            pass
        else:
            data.rename(columns={'id': 'concept_code'}, inplace=True)
            data['src'] = 'ts'
            pd.io.sql.to_sql(data, 'stock_concept_detail', con=connect, schema='gupiaowajue2', if_exists='append',
                             index=False)
            # 防止超出每分钟200次的请求上限造成程序错误
            time.sleep(0.5)
    connect.dispose()


def update_stock_area_table():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    area_i = []
    area_n = []
    area_e = []
    tree = ET.parse('SysGrp.xml')
    root = tree.getroot()
    for x in root[0][11]:
        area_i.append(x.get('i'))
        area_n.append(x.get('n'))
        area_e.append(x.get('e'))
    area_df = pd.DataFrame()
    area_df['area_code'] = area_i
    area_df['area_name'] = area_n
    area_df['area_enname'] = area_e
    pd.io.sql.to_sql(area_df, 'stock_area_list', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    connect.dispose()


def update_stock_company_extend():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    pro = ts.pro_api()
    data = pro.stock_basic(fields='ts_code')
    stock_list = data['ts_code'].tolist()
    company_extend_df = pd.DataFrame()
    from WindPy import w
    w.start()
    data = w.wss(stock_list,
                 "fax,fiscaldate,registernumber,abstract,organizationcode,address,industry_csrc12_n,industry_CSRCcode12,industry_sw,industry_swcode,auditor,clo,assetapp",
                 "tradeDate=20190301;industryType=3")
    company_extend_df['ts_code']=data.Codes
    company_extend_df['fax'] = data.Data[0]
    company_extend_df['fiscaldate'] = data.Data[1]
    company_extend_df['registernumber'] = data.Data[2]
    company_extend_df['abstract'] = data.Data[3]
    company_extend_df['organizationcode'] = data.Data[4]
    company_extend_df['address'] = data.Data[5]
    company_extend_df['industry_csrc_name'] = data.Data[6]
    company_extend_df['industry_csrc_code'] = data.Data[7]
    company_extend_df['industry_sw_name'] = data.Data[8]
    company_extend_df['industry_sw_code'] = data.Data[9]
    company_extend_df['auditor'] = data.Data[10]
    company_extend_df['clo'] = data.Data[11]
    company_extend_df['assetapp'] = data.Data[12]
    pd.io.sql.to_sql(company_extend_df, 'stock_company_extend', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    connect.dispose()


def update_stock_ipo_info():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    pro = ts.pro_api()
    data = pro.stock_basic(fields='ts_code')
    stock_list = data['ts_code'].tolist()
    ipo_info_df = pd.DataFrame()
    from WindPy import w
    w.start()
    data = w.wss(stock_list,
                 "ipo_date,ipo_price,ipo_collection,ipo_puboffrdate,ipo_leadundr,ipo_nominator,ipo_type,ipo_expense,ipo_amount,ipo_sponsorrepresentative,ipo_dilutedpe,ipo_weightedpe",
                 "unit=1")
    ipo_info_df['ts_code']=data.Codes
    ipo_info_df['ipo_date']=data.Data[0]
    ipo_info_df['ipo_price']=data.Data[1]
    ipo_info_df['ipo_collection']=data.Data[2]
    ipo_info_df['ipo_puboffrdate']=data.Data[3]
    ipo_info_df['ipo_leadundr']=data.Data[4]
    ipo_info_df['ipo_nominator']=data.Data[5]
    ipo_info_df['ipo_type']=data.Data[6]
    ipo_info_df['ipo_expense']=data.Data[7]
    ipo_info_df['ipo_amount']=data.Data[8]
    ipo_info_df['ipo_sponsorrepresentative']=data.Data[9]
    ipo_info_df['ipo_dilutedpe']=data.Data[10]
    ipo_info_df['ipo_weightedpe']=data.Data[11]
    pd.io.sql.to_sql(ipo_info_df, 'stock_ipo_info', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    connect.dispose()


def update_stock_company():
    connect = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue2?charset=utf8')
    pro = ts.pro_api()
    data = pro.stock_company(exchange='SZSE', fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
    pd.io.sql.to_sql(data, 'stock_company', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    data = pro.stock_company(exchange='SSE',
                             fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
    pd.io.sql.to_sql(data, 'stock_company', con=connect, schema='gupiaowajue2', if_exists='append',
                     index=False)
    connect.dispose()


if __name__ == '__main__':
    pass


#
# for index, row in data.iterrows():
#     stock=row['ts_code']
#     df = ts.pro_bar(pro_api=pro, ts_code=stock, adj='qfq', start_date='20050101', end_date='20181111')
#     del df['trade_date']
#     pd.io.sql.to_sql(df, 'stock_daily_bar', con=connect, schema='finmagic', if_exists='append',dtype={'ts_code':VARCHAR(255),'trade_date':VARCHAR(255)})
#     print(index)
# connect.dispose()
