a = 9999999999  # cas ve vterinach
# dny
x1 = a / 24
x2 = x1 // (60 * 60)
# hodiny
y1 = (a / (60 * 60 * 24)) - x2
y2 = (y1 * 24 * 60) // 60
# minuty
z1 = (a / (60 * 60)) - (x2 * 24) - y2
z2 = (z1 * 60 * 60) // 60
# vteriny
u1 = (a / 60) - (x2 * 24 * 60) - (y2 * 60) - z2
u2 = u1 * 60

print('dnu: {} hodin: {} minut: {} vterin: {}'.format(round(x2), round(y2), round(z2), round(u2)))
