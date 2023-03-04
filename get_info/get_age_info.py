from datetime import date, datetime
''' Возвращает возраст по дате рождения bdate.'''
def get_age(bdate):

    today_date = date.today()
    date_str = bdate
    date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
    difference_days = today_date - date_obj
    age = int((difference_days.days)/365)

    return age