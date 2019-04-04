import datetime
from webapp.models import Market_Calendar


def date_validation(date, period=30):
    date_result = Market_Calendar.query.filter_by(is_open=1).order_by(Market_Calendar.cal_date.desc()).limit(
        period).all()
    date_list = []
    for i in date_result:
        date_list.append(i.cal_date)
    if date in date_list:
        return date, date_list
    else:
        date = date_list[0]
        return date, date_list

def get_offset_date(now,day):
    now=datetime.datetime.strptime(now,'%Y%m%d')
    offset_date=now+datetime.timedelta(days=day)
    offset_date_string=offset_date.strftime('%Y%m%d')
    return offset_date_string

