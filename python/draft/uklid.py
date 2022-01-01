import calendar
import datetime

YEAR = 2022


def weekday_from_date_idx(day, month, year):
    return datetime.date(day=day, month=month, year=year).weekday()


def weekday_from_date(day, month, year):
    return calendar.day_name[
        datetime.date(day=day, month=month, year=year).weekday()
    ]


my_text_calendar = calendar.TextCalendar()
c = my_text_calendar.yeardatescalendar(YEAR)
unique_weeks = set()
for month in c:
    for week in month:
        for days in week:
            my_week = (days[calendar.MONDAY], days[calendar.SUNDAY])
            unique_weeks.add(my_week)

for w in sorted(unique_weeks):
    print('{} - {}'.format(w[0].strftime("%d.%m.%Y"), w[1].strftime("%d.%m.%Y")))
