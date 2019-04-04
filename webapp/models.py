from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, create_engine,distinct
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()
engine = create_engine('mysql+pymysql://root:0000@116.196.90.212:3306/gupiaowajue')
DBSession = sessionmaker(bind=engine)
my_session = DBSession()

class jccwsj(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jccwsj'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    sec_name=db.Column(db.String(255))
    the_date=db.Column(db.String(255),primary_key=True)
    eps_basic_is=db.Column(db.Float)
    net_cash_flows_oper_act=db.Column(db.Float)
    tot_cur_assets=db.Column(db.Float)
    tot_cur_liab=db.Column(db.Float)
    tot_profit=db.Column(db.Float)
    tot_liab=db.Column(db.Float)
    net_profit_is=db.Column(db.Float)
    oper_profit=db.Column(db.Float)
    net_incr_cash_cash_equ_dm=db.Column(db.Float)
    net_invest_inc=db.Column(db.Float)
    tot_assets=db.Column(db.Float)
    oper_cost=db.Column(db.Float)
    monetary_cap=db.Column(db.Float)
    long_term_rec=db.Column(db.Float)
    tot_non_cur_liab=db.Column(db.Float)
    inventories=db.Column(db.Float)
    cash_cash_equ_beg_period=db.Column(db.Float)
    cash_cash_equ_end_period=db.Column(db.Float)
    net_cash_flows_fnc_act=db.Column(db.Float)
    net_cash_flows_inv_act=db.Column(db.Float)
    selling_dist_exp=db.Column(db.Float)
    gerl_admin_exp=db.Column(db.Float)
    fin_exp_is=db.Column(db.Float)
    taxes_surcharges_ops=db.Column(db.Float)
    cap_stk=db.Column(db.Float)
    oper_rev=db.Column(db.Float)
    net_fixed_assets=db.Column(db.Float)
    net_non_oper_income=db.Column(db.Float)
    net_asset_per=db.Column(db.Float)
    net_cash_flows_oper_act_per=db.Column(db.Float)
    main_oper_rev=db.Column(db.Float)
    main_oper_profit=db.Column(db.Float)
    main_oper_cost=db.Column(db.Float)
    main_oper_tax=db.Column(db.Float)
    net_profit_is_excluded=db.Column(db.Float)
    tot_equity=db.Column(db.Float)
    income_tax_expenses=db.Column(db.Float)
    eps_diluted_is=db.Column(db.Float)
    tot_cost=db.Column(db.Float)
    ave_assets=db.Column(db.Float)
    sale_rev=db.Column(db.Float)
    ave_net_assets=db.Column(db.Float)
    tax_cost=db.Column(db.Float)
    non_main_oper_rec=db.Column(db.Float)
    long_term_debt=db.Column(db.Float)
    long_assets=db.Column(db.Float)
    long_capital=db.Column(db.Float)
    working_capital=db.Column(db.Float)
    intang_assets=db.Column(db.Float)
    sh_rights=db.Column(db.Float)
    sale_cost=db.Column(db.Float)
    net_cash_flow=db.Column(db.Float)
    rate_rec_on_net_asset=db.Column(db.Float)
class jccwzb(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jccwzb'
    index = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    sec_name=db.Column(db.String(255))
    date=db.Column(db.String(255),primary_key=True)
    rate_return_on_tot_asset=db.Column(db.Float)
    rate_return_on_cost=db.Column(db.Float)
    net_profit_margin=db.Column(db.Float)
    rate_return_on_net_asset=db.Column(db.Float)
    three_cost_proportion=db.Column(db.Float)
    pro_margin_main_business=db.Column(db.Float)
    oper_profit_margin=db.Column(db.Float)
    rate_return_on_equity=db.Column(db.Float)
    rate_return_on_asset=db.Column(db.Float)
    non_main_proportion=db.Column(db.Float)
    rate_net_return_on_tot_asset=db.Column(db.Float)
    cost_rate_main_business=db.Column(db.Float)
    rate_equity_reward=db.Column(db.Float)
    rate_gross_sales_interest=db.Column(db.Float)
    ratio_main_profit=db.Column(db.Float)
    ratio_current=db.Column(db.Float)
    ratio_long_debts_working_captial=db.Column(db.Float)
    ratio_long_assets_long_captial=db.Column(db.Float)
    ratio_liquidation_value=db.Column(db.Float)
    ratio_quick=db.Column(db.Float)
    ratio_sh_equity=db.Column(db.Float)
    ratio_capitalization=db.Column(db.Float)
    ratio_share_equity=db.Column(db.Float)
    ratio_cash=db.Column(db.Float)
    ratio_long_debt=db.Column(db.Float)
    ration_net_value_fixed_assets=db.Column(db.Float)
    ratio_interest_coverage=db.Column(db.Float)
    ration_sh_right_fixed_assets=db.Column(db.Float)
    ratio_capital_immobilization=db.Column(db.Float)
    ratio_asset_liability=db.Column(db.Float)
    ratio_debt_right=db.Column(db.Float)
    ratio_property_right=db.Column(db.Float)
    growth_rate_main_business_income=db.Column(db.Float)
    growth_rate_net_profit=db.Column(db.Float)
    growth_rate_net_assets=db.Column(db.Float)
    growth_rate_tot_assets=db.Column(db.Float)
    rate_receivable_turnover=db.Column(db.Float)
    days_inventory_turnover_oper_income=db.Column(db.Float)
    rate_assets_oper_cash_flow=db.Column(db.Float)
    days_receivable_turnover=db.Column(db.Float)
    days_tot_assets_turnover=db.Column(db.Float)
    ratio_oper_cash_net_profit=db.Column(db.Float)
    ratio_inventory_turnover=db.Column(db.Float)
    ratio_current_assets_turnover=db.Column(db.Float)
    ratio_oper_cash_debt=db.Column(db.Float)
    ratio_fixed_assets_turnover=db.Column(db.Float)
    days_current_assets_turnover=db.Column(db.Float)
    ratio_cash_flow=db.Column(db.Float)
    ratio_tot_assets_turnover=db.Column(db.Float)
    ratio_net_assets = db.Column(db.Float)
    ratio_fixed_assets = db.Column(db.Float)
    ratio_oper_cash_income=db.Column(db.Float)
class lrbzy(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'lrbzy'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source=db.Column(db.String(255))
class zcfzbzy(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'zcfzbzy'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class xjllbzy(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'xjllbzy'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class cwbg(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'cwbg'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class ylnl(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'ylnl'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class chnl(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'chnl'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class cznl(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'cznl'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class yynl(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'yynl'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class zycwzb(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'zycwzb'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class jcsj_gsgk(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_gsgk'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    full_name=db.Column(db.String(255))
    website=db.Column(db.String(255))
    eng_name=db.Column(db.String(255))
    short_name=db.Column(db.String(255))
    address=db.Column(db.String(255))
    legal_representative=db.Column(db.String(255))
    boardchairmen=db.Column(db.String(255))
    regist_captial=db.Column(db.String(255))
    industry=db.Column(db.String(255))
    phone=db.Column(db.String(255))
    fax=db.Column(db.String(255))
    raise_date=db.Column(db.String(255))
    exch_date=db.Column(db.String(255))
    pub_num=db.Column(db.Integer)
    pub_style=db.Column(db.String(255))
    pub_price=db.Column(db.Float)
    pub_ttm=db.Column(db.Float)
    main_underwriter=db.Column(db.String(255))
    to_underwriter=db.Column(db.String(255))
    exch_sponsors=db.Column(db.String(255))
    sponsor_agency=db.Column(db.String(255))
class jcsj_fxcz(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_fxcz'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    pub_type=db.Column(db.String(255))
    pub_date=db.Column(db.String(255))
    pub_character=db.Column(db.String(255))
    pub_stock_type=db.Column(db.String(255))
    pub_style=db.Column(db.String(255))
    pub_stock_num=db.Column(db.Integer)
    pub_price_cns=db.Column(db.Float)
    pub_price_fore=db.Column(db.Float)
    act_fund=db.Column(db.Float)
    act_cost=db.Column(db.Float)
    pub_ttm=db.Column(db.Float)
    lot_rate_oniline_pricing=db.Column(db.Float)
    bid_rate_sec_distribution=db.Column(db.Float)
class jcsj_fhpg(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_fxpg'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    bonus_year=db.Column(db.String(255))
    bonus_plan=db.Column(db.String(255))
    date_equity_regist=db.Column(db.String(255))
    date_exclusion=db.Column(db.String(255))
    date_bonus_shares=db.Column(db.String(255))
class jcsj_ggry(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_ggry'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    name=db.Column(db.String(255),primary_key=True)
    birth_year=db.Column(db.String(255),primary_key=True)
    education=db.Column(db.String(255))
    sex=db.Column(db.String(255),primary_key=True)
    post=db.Column(db.String(255))
class jcsj_sdgd(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_sdgd'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    name=db.Column(db.String(255),primary_key=True)
    num=db.Column(db.Float)
    ratio=db.Column(db.Float)
    type=db.Column(db.String(255))
class jcsj_ltgd(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_ltgd'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    name=db.Column(db.String(255),primary_key=True)
    num = db.Column(db.Float)
    ratio = db.Column(db.Float)
    type=db.Column(db.String(255))
class jcsj_zczd(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_zczd'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    type=db.Column(db.String(255))
    title=db.Column(db.String(255),primary_key=True)
class jcsj_gsgg(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_gsgg'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    title=db.Column(db.String(255),primary_key=True)
    type=db.Column(db.String(255))
class jcsj_ggzx(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_ggzx'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    title=db.Column(db.String(255),primary_key=True)
    time=db.Column(db.String(255))
class jcsj_hyzx(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_hyzx'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    title=db.Column(db.String(255),primary_key=True)
    time=db.Column(db.String(255))
class jcsj_hdcf(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcsj_hdcf'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    title=db.Column(db.String(255),primary_key=True)
    type=db.Column(db.String(255))
class bkqj_cndtqj(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'bkqj_cndtqj'
    index = db.Column(db.Integer)
    industry_name=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    transaction_capital=db.Column(db.Float)
    ave_turnover_rate=db.Column(db.Float)
    ave_up_downs=db.Column(db.Float)
    cur_market_value=db.Column(db.Float)
    ave_ttm=db.Column(db.Float)
class bkqj_cndtqj_region(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'bkqj_cndtqj_region'
    region_name=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    transaction_capital=db.Column(db.Float)
    ave_turnover_rate=db.Column(db.Float)
    ave_up_downs=db.Column(db.Float)
    cur_market_value=db.Column(db.Float)
class bkqj_cndtqj_conceptual(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'bkqj_cndtqj_conceptual'
    conceptual_name=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    transaction_capital=db.Column(db.Float)
    ave_turnover_rate=db.Column(db.Float)
    ave_up_downs=db.Column(db.Float)
    cur_market_value=db.Column(db.Float)
class bkqj_cwdtqj(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'bkqj_cwdtqj'
    id = db.Column(db.Integer)
    industry_name=db.Column(db.String(255),primary_key=True)
    date=db.Column(db.String(255),primary_key=True)
    all_click_num=db.Column(db.Integer)
    post_num=db.Column(db.Integer)
class bkqj_cwzbbj(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'bkqj_cwzbbj'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class bkqj_hqsjbj(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'bkqj_hqsjbj'
    id = db.Column(db.Integer)
    index_cns_name=db.Column(db.String(255))
    index_eng_name=db.Column(db.String(255),primary_key=True)
    data_source = db.Column(db.String(255))
class jcrxsj(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'jcrxsj'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    ts_name=db.Column(db.String(255))
    trade_date=db.Column(db.String(255),primary_key=True)
    pct_change = db.Column(db.Float)
    current=db.Column(db.Float)
    open=db.Column(db.Float)
    high=db.Column(db.Float)
    low=db.Column(db.Float)
    pre_close=db.Column(db.Float)
    turnover_rate=db.Column(db.Float)
    vol=db.Column(db.Float)
    amount=db.Column(db.Float)
    cir_value=db.Column(db.Float)
    pe_ttm=db.Column(db.Float)
    pb=db.Column(db.Float)
    market_value=db.Column(db.Float)
    score=db.Column(db.Float)
class gpjbxx(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'gpjbxx'
    id = db.Column(db.Integer)
    ts_code=db.Column(db.String(255),primary_key=True)
    ts_name=db.Column(db.String(255))
    industry=db.Column(db.String(255))
    area = db.Column(db.String(255))
    conceptual_plate=db.Column(db.String(255))
class qjzn(db.Model):
    __bind_key__ = 'gupiaowajue'
    __tablename__ = 'qjzn'
    stock_code=db.Column(db.String(255),primary_key=True)
    industry2=db.Column(db.String(255))
    concept=db.Column(db.String(255))
    province = db.Column(db.String(255))
    city=db.Column(db.String(255))
class region(db.Model):
    __tablename__ = 'region'
    region_name = db.Column(db.String(255), primary_key=True)
    id = db.Column(db.String(255))



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    emailaddress = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    username = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    active = db.Column(db.Boolean)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def is_active(self):
        return self.active

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_avatar(self):
        return self.avatar


class DB_ENV(db.Model):
    __tablename__ = 'db_env'
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class DB_LOG(db.Model):
    __tablename__ = 'db_log'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    commit_time = db.Column(db.String(255))
    start_time = db.Column(db.String(255))
    finish_time = db.Column(db.String(255))
    status = db.Column(db.String(255))
    error = db.Column(db.String(255))
    admin_id = db.Column(db.String(255))


class DB_TABLES(db.Model):
    __tablename__ = 'db_tables'
    table_name = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.Text)
    update_time = db.Column(db.String(255))


class Market_Calendar(db.Model):
    __tablename__ = 'market_calendar'
    cal_date = db.Column(db.String(255), primary_key=True)
    is_open = db.Column(db.Integer)
    exchange = db.Column(db.String(255))


class Market_Money_Flow(db.Model):
    __tablename__ = 'market_money_flow'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    buy_sm_vol = db.Column(db.Float)
    buy_sm_amount = db.Column(db.Float)
    sell_sm_vol = db.Column(db.Float)
    sell_sm_amount = db.Column(db.Float)
    buy_md_vol = db.Column(db.Float)
    buy_md_amount = db.Column(db.Float)
    sell_md_vol = db.Column(db.Float)
    sell_md_amount = db.Column(db.Float)
    buy_lg_vol = db.Column(db.Float)
    buy_lg_amount = db.Column(db.Float)
    sell_lg_vol = db.Column(db.Float)
    sell_lg_amount = db.Column(db.Float)
    buy_elg_vol = db.Column(db.Float)
    buy_elg_amount = db.Column(db.Float)
    sell_elg_vol = db.Column(db.Float)
    sell_elg_amount = db.Column(db.Float)
    net_mf_vol = db.Column(db.Float)
    net_mf_amount = db.Column(db.Float)


class Model_Associate_Rule(db.Model):
    __tablename__ = 'model_associate_rule'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    associate_code = db.Column(db.String(255), primary_key=True)
    trading_day_count = db.Column(db.Integer)
    matching_day_count = db.Column(db.Integer)
    effect_day_count = db.Column(db.Integer)
    associate_type = db.Column(db.String(255))
    approval_rating = db.Column(db.Float)
    probability = db.Column(db.Float)


class Model_Correlation_Short_Term(db.Model):
    __tablename__ = 'model_correlation_short_term'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    correlation_1_code = db.Column(db.String(255))
    correlation_1_r = db.Column(db.Float)
    correlation_1_matching_start_time = db.Column(db.String(255))
    correlation_1_matching_end_time = db.Column(db.String(255))
    correlation_1_prediction_start_time = db.Column(db.String(255))
    correlation_1_prediction_end_time = db.Column(db.String(255))
    correlation_1_change = db.Column(db.Float)
    correlation_1_trend_description = db.Column(db.String(255))
    correlation_2_code = db.Column(db.String(255))
    correlation_2_r = db.Column(db.Float)
    correlation_2_matching_start_time = db.Column(db.String(255))
    correlation_2_matching_end_time = db.Column(db.String(255))
    correlation_2_prediction_start_time = db.Column(db.String(255))
    correlation_2_prediction_end_time = db.Column(db.String(255))
    correlation_2_change = db.Column(db.Float)
    correlation_2_trend_description = db.Column(db.String(255))
    correlation_3_code = db.Column(db.String(255))
    correlation_3_r = db.Column(db.Float)
    correlation_3_matching_start_time = db.Column(db.String(255))
    correlation_3_matching_end_time = db.Column(db.String(255))
    correlation_3_prediction_start_time = db.Column(db.String(255))
    correlation_3_prediction_end_time = db.Column(db.String(255))
    correlation_3_change = db.Column(db.Float)
    correlation_3_trend_description = db.Column(db.String(255))


class Model_Fluctuation_Correlation(db.Model):
    __tablename__ = 'model_fluctuation_correlation'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    D4 = db.Column(db.Integer)
    D3 = db.Column(db.Integer)
    D2 = db.Column(db.Integer)
    D1 = db.Column(db.Integer)
    five_sample_count = db.Column(db.Integer)
    five_total_count = db.Column(db.Integer)
    five_approval_rating = db.Column(db.Float)
    five_D0_list = db.Column(db.BLOB)
    five_appearance_count_list = db.Column(db.BLOB)
    five_proportion_list = db.Column(db.BLOB)
    four_sample_count = db.Column(db.Integer)
    four_total_count = db.Column(db.Integer)
    four_approval_rating = db.Column(db.Float)
    four_D0_list = db.Column(db.BLOB)
    four_appearance_count_list = db.Column(db.BLOB)
    four_proportion_list = db.Column(db.BLOB)
    three_sample_count = db.Column(db.Integer)
    three_total_count = db.Column(db.Integer)
    three_approval_rating = db.Column(db.Float)
    three_D0_list = db.Column(db.BLOB)
    three_appearance_count_list = db.Column(db.BLOB)
    three_proportion_list = db.Column(db.BLOB)
    two_sample_count = db.Column(db.Integer)
    two_total_count = db.Column(db.Integer)
    two_approval_rating = db.Column(db.Float)
    two_D0_list = db.Column(db.BLOB)
    two_appearance_count_list = db.Column(db.BLOB)
    two_proportion_list = db.Column(db.BLOB)


class Model_Fluctuation_Sequencing(db.Model):
    __tablename__ = 'model_fluctuation_sequencing'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    close = db.Column(db.Float)
    history_high = db.Column(db.Float)
    history_low = db.Column(db.Float)
    high_change = db.Column(db.Float)
    high_order = db.Column(db.Integer)
    low_change = db.Column(db.Float)
    low_order = db.Column(db.Integer)
    order_sum = db.Column(db.Integer)


class Model_Fluctuation_Statistics(db.Model):
    __tablename__ = 'model_fluctuation_statistics'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    D4 = db.Column(db.Integer)
    D3 = db.Column(db.Integer)
    D2 = db.Column(db.Integer)
    D1 = db.Column(db.Integer)
    five_total_count = db.Column(db.Integer)
    five_D0_list = db.Column(db.BLOB)
    five_appearance_count_list = db.Column(db.BLOB)
    five_proportion_list = db.Column(db.BLOB)
    four_total_count = db.Column(db.Integer)
    four_D0_list = db.Column(db.BLOB)
    four_appearance_count_list = db.Column(db.BLOB)
    four_proportion_list = db.Column(db.BLOB)
    three_total_count = db.Column(db.Integer)
    three_D0_list = db.Column(db.BLOB)
    three_appearance_count_list = db.Column(db.BLOB)
    three_proportion_list = db.Column(db.BLOB)
    two_total_count = db.Column(db.Integer)
    two_D0_list = db.Column(db.BLOB)
    two_appearance_count_list = db.Column(db.BLOB)
    two_proportion_list = db.Column(db.BLOB)
    one_total_count = db.Column(db.Integer)
    one_D0_list = db.Column(db.BLOB)
    one_appearance_count_list = db.Column(db.BLOB)
    one_proportion_list = db.Column(db.BLOB)


class Model_Similarity_Fluctuation(db.Model):
    __tablename__ = 'model_similarity_fluctuation'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    stock_list = db.Column(db.BLOB)
    liveness_list = db.Column(db.BLOB)


class Model_Similarity_History(db.Model):
    __tablename__ = 'model_similarity_history'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    matching_start_time = db.Column(db.String(255))
    matching_end_time = db.Column(db.String(255))
    prediction_start_time = db.Column(db.String(255))
    prediction_end_time = db.Column(db.String(255))
    distance = db.Column(db.Float)
    change = db.Column(db.Float)
    trend_description = db.Column(db.String(255))


class Model_Similarity_Short_Term(db.Model):
    __tablename__ = 'model_similarity_short_term'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    similarity_1_code = db.Column(db.String(255))
    similarity_1_distance = db.Column(db.Float)
    similarity_1_matching_start_time = db.Column(db.String(255))
    similarity_1_matching_end_time = db.Column(db.String(255))
    similarity_1_prediction_start_time = db.Column(db.String(255))
    similarity_1_prediction_end_time = db.Column(db.String(255))
    similarity_1_change = db.Column(db.Float)
    similarity_1_trend_description = db.Column(db.String(255))
    similarity_2_code = db.Column(db.String(255))
    similarity_2_distance = db.Column(db.Float)
    similarity_2_matching_start_time = db.Column(db.String(255))
    similarity_2_matching_end_time = db.Column(db.String(255))
    similarity_2_prediction_start_time = db.Column(db.String(255))
    similarity_2_prediction_end_time = db.Column(db.String(255))
    similarity_2_change = db.Column(db.Float)
    similarity_2_trend_description = db.Column(db.String(255))
    similarity_3_code = db.Column(db.String(255))
    similarity_3_distance = db.Column(db.Float)
    similarity_3_matching_start_time = db.Column(db.String(255))
    similarity_3_matching_end_time = db.Column(db.String(255))
    similarity_3_prediction_start_time = db.Column(db.String(255))
    similarity_3_prediction_end_time = db.Column(db.String(255))
    similarity_3_change = db.Column(db.Float)
    similarity_3_trend_description = db.Column(db.String(255))


class Model_Similarity_Trend(db.Model):
    __tablename__ = 'model_similarity_trend'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    stock_list = db.Column(db.BLOB)
    liveness_list = db.Column(db.BLOB)


class Model_State_Transition(db.Model):
    __tablename__ = 'model_state_transition'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    s_rise_rate = db.Column(db.Float)
    s_maintain_rate = db.Column(db.Float)
    s_fall_rate = db.Column(db.Float)
    l_rise_rate = db.Column(db.Float)
    l_maintain_rate = db.Column(db.Float)
    l_fall_rate = db.Column(db.Float)


class Model_Stock_Assessment(db.Model):
    __tablename__ = 'model_stock_assessment'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    estimated_value = db.Column(db.Float)
    estimated_value_std = db.Column(db.Float)
    similar_pe_count = db.Column(db.Integer)
    pe_mean = db.Column(db.Float)
    pe_std = db.Column(db.Float)
    pe_max = db.Column(db.Float)
    pe_min = db.Column(db.Float)


class Model_Trading_Point(db.Model):
    __tablename__ = 'model_trading_point'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    aggressive_buy_point = db.Column(db.Boolean)
    aggressive_sell_point = db.Column(db.Boolean)
    aggressive_buy_requirement = db.Column(db.String(255))
    aggressive_sell_requirement = db.Column(db.String(255))
    steady_buy_point = db.Column(db.Boolean)
    steady_sell_point = db.Column(db.Boolean)
    steady_buy_requirement = db.Column(db.String(255))
    steady_sell_requirement = db.Column(db.String(255))


class Model_Trend_Forecast(db.Model):
    __tablename__ = 'model_trend_forecast'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    first_change = db.Column(db.Float)
    first_rise_vote = db.Column(db.Integer)
    first_maintain_vote = db.Column(db.Integer)
    first_fall_vote = db.Column(db.Integer)
    second_change = db.Column(db.Float)
    second_rise_vote = db.Column(db.Integer)
    second_maintain_vote = db.Column(db.Integer)
    second_fall_vote = db.Column(db.Integer)
    third_change = db.Column(db.Float)
    third_rise_vote = db.Column(db.Integer)
    third_maintain_vote = db.Column(db.Integer)
    third_fall_vote = db.Column(db.Integer)


class Stock_Area_List(db.Model):
    __tablename__ = 'stock_area_list'
    area_code = db.Column(db.String(255), primary_key=True)
    area_name = db.Column(db.String(255))
    area_enname = db.Column(db.String(255))


class Stock_Basic(db.Model):
    __tablename__ = 'stock_basic'
    ts_code = db.Column(db.String(255), primary_key=True)
    symbol = db.Column(db.String(255))
    name = db.Column(db.String(255))
    abbreviation = db.Column(db.String(255))
    area = db.Column(db.String(255))
    industry = db.Column(db.String(255))
    fullname = db.Column(db.Text)
    enname = db.Column(db.Text)
    market = db.Column(db.String(255))
    exchange = db.Column(db.String(255))
    curr_type = db.Column(db.String(255))
    list_status = db.Column(db.String(255))
    list_date = db.Column(db.String(255))
    delist_date = db.Column(db.String(255))
    is_hs = db.Column(db.String(255))


class Stock_Company(db.Model):
    __tablename__ = 'stock_company'
    ts_code = db.Column(db.String(255), primary_key=True)
    exchange = db.Column(db.String(255))
    chairman = db.Column(db.String(255))
    manager = db.Column(db.String(255))
    secretary = db.Column(db.String(255))
    reg_capital = db.Column(db.Float)
    setup_date = db.Column(db.String(255))
    province = db.Column(db.String(255))
    city = db.Column(db.String(255))
    introduction = db.Column(db.Text)
    website = db.Column(db.String(255))
    email = db.Column(db.String(255))
    office = db.Column(db.String(255))
    employees = db.Column(db.Integer)
    main_business = db.Column(db.Text)
    business_scope = db.Column(db.Text)


class Stock_Company_Extend(db.Model):
    __tablename__ = 'stock_company_extend'
    ts_code = db.Column(db.String(255), primary_key=True)
    abstract = db.Column(db.String(255))
    fax = db.Column(db.String(255))
    address = db.Column(db.String(255))
    fiscaldate = db.Column(db.String(255))
    registernumber = db.Column(db.String(255))
    organizationcode = db.Column(db.String(255))
    industry_csrc_name = db.Column(db.String(255))
    industry_csrc_code = db.Column(db.String(255))
    industry_sw_name = db.Column(db.String(255))
    industry_sw_code = db.Column(db.String(255))
    auditor = db.Column(db.String(255))
    clo = db.Column(db.String(255))
    assetapp = db.Column(db.String(255))


class Stock_Concept_Detail(db.Model):
    __tablename__ = 'stock_concept_detail'
    concept_code = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    in_date = db.Column(db.String(255))
    out_date = db.Column(db.String(255))
    src = db.Column(db.String(255))


class Stock_Concept_List(db.Model):
    __tablename__ = 'stock_concept_list'
    concept_code = db.Column(db.String(255), primary_key=True)
    concept_name = db.Column(db.String(255))
    concept_enname = db.Column(db.String(255))
    src = db.Column(db.String(255))


class Stock_Daily_Bar(db.Model):
    __tablename__ = 'stock_daily_bar'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    pre_close = db.Column(db.Float)
    change = db.Column(db.Float)
    pct_chg = db.Column(db.Float)
    vol = db.Column(db.Float)
    amount = db.Column(db.Float)


class Stock_Daily_Basic(db.Model):
    __tablename__ = 'stock_daily_basic'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    close = db.Column(db.Float)
    turnover_rate = db.Column(db.Float)
    turnover_rate_f = db.Column(db.Float)
    volume_ratio = db.Column(db.Float)
    pe = db.Column(db.Float)
    pe_ttm = db.Column(db.Float)
    pb = db.Column(db.Float)
    ps = db.Column(db.Float)
    ps_ttm = db.Column(db.Float)
    total_share = db.Column(db.Float)
    float_share = db.Column(db.Float)
    free_share = db.Column(db.Float)
    total_mv = db.Column(db.Float)
    circ_mv = db.Column(db.Float)


class Stock_Daily_Basic_Extend(db.Model):
    __tablename__ = 'stock_daily_basic_extend'
    trade_date = db.Column(db.String(255), primary_key=True)
    ts_code = db.Column(db.String(255), primary_key=True)
    gr_ttm = db.Column(db.Float)
    or_ttm = db.Column(db.Float)
    profit_ttm = db.Column(db.Float)
    netprofit_ttm = db.Column(db.Float)
    deductedprofit_ttm = db.Column(db.Float)
    equity_new = db.Column(db.Float)
    operatecashflow_ttm = db.Column(db.Float)
    cashflow_ttm = db.Column(db.Float)
    eps_ttm = db.Column(db.Float)
    ocfps_ttm = db.Column(db.Float)
    orps_ttm = db.Column(db.Float)
    cfps_ttm = db.Column(db.Float)


class Stock_HS_Const(db.Model):
    __tablename__ = 'stock_hs_const'
    ts_code = db.Column(db.String(255), primary_key=True)
    hs_type = db.Column(db.String(255))
    in_date = db.Column(db.String(255))
    out_date = db.Column(db.String(255))
    is_new = db.Column(db.String(255))


class Stock_Industry_Basic(db.Model):
    __tablename__ = 'stock_industry_basic'
    trade_date = db.Column(db.String(255), primary_key=True)
    industry_code = db.Column(db.String(255), primary_key=True)
    pe_avg = db.Column(db.Float)
    pe_ttm_overall = db.Column(db.Float)
    pe_ttm_avg = db.Column(db.Float)
    pb_overall = db.Column(db.Float)
    pb_avg = db.Column(db.Float)
    mkt_cap_float_a_shares_sum = db.Column(db.Float)
    pct_chg_avg = db.Column(db.Float)
    pct_chg_tmc_wavg = db.Column(db.Float)
    turn_avg = db.Column(db.Float)
    turn_tmc_wavg = db.Column(db.Float)
    vol_sum = db.Column(db.Float)
    amount_sum = db.Column(db.Float)
    csrc_company_num = db.Column(db.Integer)
    csrc_pe = db.Column(db.Float)
    csrc_pe_ttm = db.Column(db.Float)
    csrc_pb = db.Column(db.Float)


class Stock_Industry_CSRC_1(db.Model):
    __tablename__ = 'stock_industry_csrc_1'
    industry_csrc_1_code = db.Column(db.String(255), primary_key=True)
    industry_csrc_1_name = db.Column(db.String(255))
    industry_csrc_1_enname = db.Column(db.String(255))


class Stock_Industry_CSRC_2(db.Model):
    __tablename__ = 'stock_industry_csrc_2'
    industry_csrc_2_code = db.Column(db.String(255), primary_key=True)
    industry_csrc_2_name = db.Column(db.String(255))
    industry_csrc_2_enname = db.Column(db.String(255))
    belong_to = db.Column(db.String(255))


class Stock_Industry_SW_1(db.Model):
    __tablename__ = 'stock_industry_sw_1'
    industry_sw_1_code = db.Column(db.String(255), primary_key=True)
    industry_sw_1_name = db.Column(db.String(255))
    industry_sw_1_enname = db.Column(db.String(255))


class Stock_Industry_SW_2(db.Model):
    __tablename__ = 'stock_industry_sw_2'
    industry_sw_2_code = db.Column(db.String(255), primary_key=True)
    industry_sw_2_name = db.Column(db.String(255))
    industry_sw_2_enname = db.Column(db.String(255))
    belong_to = db.Column(db.String(255))


class Stock_Industry_SW_3(db.Model):
    __tablename__ = 'stock_industry_sw_3'
    industry_sw_3_code = db.Column(db.String(255), primary_key=True)
    industry_sw_3_name = db.Column(db.String(255))
    industry_sw_3_enname = db.Column(db.String(255))
    belong_to = db.Column(db.String(255))


class Stock_IPO_Info(db.Model):
    __tablename__ = 'stock_ipo_info'
    ts_code = db.Column(db.String(255), primary_key=True)
    ipo_date = db.Column(db.String(255))
    ipo_price = db.Column(db.Float)
    ipo_collection = db.Column(db.Float)
    ipo_puboffrdate = db.Column(db.String(255))
    ipo_leadundr = db.Column(db.String(255))
    ipo_nominator = db.Column(db.String(255))
    ipo_sponsorrepresentative = db.Column(db.String(255))
    ipo_type = db.Column(db.String(255))
    ipo_expense = db.Column(db.Float)
    ipo_amount = db.Column(db.Float)
    ipo_dilutedpe = db.Column(db.Float)
    ipo_weightedpe = db.Column(db.Float)


class Stock_New_Share(db.Model):
    __tablename__ = 'stock_new_share'
    ts_code = db.Column(db.String(255), primary_key=True)
    sub_code = db.Column(db.String(255))
    name = db.Column(db.String(255))
    ipo_date = db.Column(db.String(255))
    issue_date = db.Column(db.String(255))
    amount = db.Column(db.Float)
    market_amount = db.Column(db.Float)
    price = db.Column(db.Float)
    pe = db.Column(db.Float)
    limit_amount = db.Column(db.Float)
    funds = db.Column(db.Float)
    ballot = db.Column(db.Float)
