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

# Show every month
for month in range(1, 13):

    # Compute the dates for each week that overlaps the month
    c = calendar.monthcalendar(YEAR, month)
    # c = my_text_calendar.monthdayscalendar(YEAR, month)
    for week in c:
        if week[calendar.MONDAY] and week[calendar.SUNDAY]:  # full week
            start_day = week[calendar.MONDAY]
            start_idx = week.index(start_day)
            start_day_name = calendar.day_name[start_idx]
            end_day = week[calendar.SUNDAY]
            end_idx = week.index(end_day)
            end_day_name = calendar.day_name[end_idx]
        else:
            # first non-zero index
            first_day_idx = week.index(next(filter(lambda x: x != 0, week)))
            # first_day_idx = week.index(1)
            start_day = week[first_day_idx]
            start_day_name = calendar.day_name[first_day_idx]
            last_day_idx = week.index(next(filter(lambda x: x == 0, week)))
            end_day = week[last_day_idx - 1]
            # end_idx = week.index(end)
            end_day_name = calendar.day_name[last_day_idx - 1]
            # print('week {}'.format(week))
        print('week {} : {}.{}.{} ({}) - {}.{}.{} ({})'.
              format(week, start_day, month, YEAR, start_day_name, end_day, month, YEAR, end_day_name))
