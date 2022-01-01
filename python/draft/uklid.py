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
flats = range(1, 17)
flat_name = {1: 'Macoun', 2: 'Havrdova', 3: 'Nosková', 4: 'Hnidková', 5: 'Bahník', 6: 'Veber', 7: 'Matura',
             8: 'Nevim', 9: 'Nevim', 10: 'Nevim', 11: 'Nevim', 12: 'Nevim', 13: 'Nevim', 14: 'Nevim', 15: 'Pekařová',
             16: 'Kopal'}
unique_weeks = set()
for month in c:
    for week in month:
        for days in week:
            my_week = (days[calendar.MONDAY], days[calendar.SUNDAY])
            unique_weeks.add(my_week)

# week_flat = list(zip(sorted(unique_weeks), itertools.cycle(flats)))
week_flat = list(zip(sorted(unique_weeks), flats))


def str_weeks(weeks):
    ret_val = ''
    for x in weeks:
        ret_val += x[0].strftime("%d.%m.%Y") + '-' + x[1].strftime("%d.%m.%Y") + ' '
    return ret_val.strip()


out_file = 'uklid.csv'
with open(out_file, "w", encoding='utf-8') as csv_file:
    csv_file.write('Jmeno\tUklid\n')
    for f in flats:
        w = [x[0] for x in week_flat if x[1] == f]
        name = flat_name[f]
        csv_file.write(name + '\t' + str_weeks(w) + '\n')
        print('{}\t{}'.format(name, str_weeks(w)))

# out_file_md = 'uklid.md'
# df = pd.read_csv(out_file)
# with open(out_file_md, 'w', encoding='utf-8') as md:
#     df.to_markdown(md, index=False)

# for w_f in week_flat:
#     w = w_f[0]
#     f = w_f[1]
#     name = flat_name[f]
#     print('{}: {} - {}'.format(name, w[0].strftime("%d.%m.%Y"), w[1].strftime("%d.%m.%Y")))
