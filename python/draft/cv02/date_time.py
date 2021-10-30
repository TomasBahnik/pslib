# Napište program, který načte celé číslo udávající časový interval ve vteřinách a vypíše kolik je to dní, hodin, minut a vteřin.
# Tedy pokud bude vstup 100000 pak vypíše: den 1 hodin 3 minut 46 vterin 40
import sys

DAY = 86400  # in sec
HOUR = 3600
MINUTE = 60

interval = 100000  # in sec
# interval = DAY  # in sec

after_days = interval % DAY
d = (interval - after_days) // DAY

after_hours = after_days % HOUR
h = (after_days - after_hours) // HOUR

after_minutes = after_hours % MINUTE  # sec
m = (after_hours - after_minutes) // MINUTE

print("day : {}, hour {}, minute {}, sec {}".format(d, h, m, after_minutes))
sys.exit(0)
