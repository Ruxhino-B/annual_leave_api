import datetime
#from holidays.models import Hollidays


#print(Hollidays.objects.get(id=1))
day_off = [datetime.date(2021, 6, 5), datetime.date(2021, 6, 15), datetime.date(2021, 6, 17), datetime.date(2021, 6, 21), datetime.date(2021, 6, 27), datetime.date(2021, 7, 1), datetime.date(2021, 7, 11), datetime.date(2021, 8, 12)]
def convert_days(fillim_date=datetime.datetime(2021, 6, 1, 9, 16, 56, 858953), fund_data=datetime.datetime(2021, 6, 1, 23, 5, 8, 206998)):
    total_date = fund_data - fillim_date
    if total_date.days > 0:
        delta = fund_data.date() - fillim_date.date()
        days_list = []
        for i in range(delta.days + 1):
            day = fillim_date.date() + datetime.timedelta(days=i)
            days_list.append(day)
        for holidays in days_list:
            if holidays.isoweekday() in range(5, 8):
                days_list.remove(holidays)
            print(holidays)
        for dit_req in days_list:
            for dit_off in day_off:
                if dit_req == dit_off:
                    days_list.remove(dit_req)
        nr_oresh = len(days_list) * 8
        return nr_oresh
    else:
        total_hours = total_date.total_seconds()/3600
        if total_hours > 8:
            total_hours = 8
        return total_hours


fillim_date1 = datetime.datetime(2021, 6, 1, 9, 16, 56, 858953)
fund_date1 = datetime.datetime(2021, 6, 3, 23, 5, 8, 206998)
list_data = []


print(convert_days())