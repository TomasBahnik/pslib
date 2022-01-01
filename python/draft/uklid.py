import calendar
import datetime
import itertools

YEAR = 2022


def weekday_from_date_idx(day, month, year):
    return datetime.date(day=day, month=month, year=year).weekday()


def weekday_from_date(day, month, year):
    return calendar.day_name[
        datetime.date(day=day, month=month, year=year).weekday()
    ]


my_text_calendar = calendar.TextCalendar()
c = my_text_calendar.yeardatescalendar(YEAR)
flats = range(1, 17)
flat_name = {1: 'Macoun', 2: 'Havrdova', 3: 'Noskova', 4: 'Hnidkova', 5: 'Bahnik', 6: 'Veber', 7: 'Matura',
             8: 'Nevim', 9: 'Nevim', 10: 'Nevim', 11: 'Nevim', 12: 'Nevim', 13: 'Nevim', 14: 'Nevim', 15: 'Pekar',
             16: 'Kopal'}
unique_weeks = set()
for month in c:
    for week in month:
        for days in week:
            my_week = (days[calendar.MONDAY], days[calendar.SUNDAY])
            unique_weeks.add(my_week)

week_flat = zip(sorted(unique_weeks), itertools.cycle(flats))

for w_f in week_flat:
    w = w_f[0]
    f = w_f[1]
    name = flat_name[f]
    print('{}: {} - {}'.format(name, w[0].strftime("%d.%m.%Y"), w[1].strftime("%d.%m.%Y")))
