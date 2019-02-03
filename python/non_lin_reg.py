from gekko import GEKKO
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["axes.spines.right"] = False
mpl.rcParams["axes.spines.top"] = False
# xm = np.array([0,1,2,3,4,5])
xm = np.array([1, 2, 3, 4, 5, 6, 7.5, 12.4, 13])
ym = np.array([10, 25, 35, 43, 47, 52, 54, 55, 55.5])

#### Solution
m = GEKKO()
m.options.IMODE = 2
# coefficients
print('x size : {}'.format(xm.size))
# 4 is size of c array
size_of_c_array = 6
c = [m.FV(value=0) for i in range(size_of_c_array)]
x = m.Param(value=xm)
y = m.CV(value=ym)
y.FSTATUS = 1
# polynomial model
m.Equation(y == c[0] + c[1] * x + c[2] * x ** 2 + c[3] * x ** 3 + c[4] * x ** 4 + c[5] * x ** 5)

# linear regression
c[0].STATUS = 1
c[1].STATUS = 1
# m.solve(disp=False)
# p1 = [c[1].value[0], c[0].value[0]]

# quadratic
c[2].STATUS = 1
# m.solve(disp=False)
# p2 = [c[2].value[0], c[1].value[0], c[0].value[0]]

# cubic
c[3].STATUS = 1
# m.solve(disp=False)
# p3 = [c[3].value[0], c[2].value[0], c[1].value[0], c[0].value[0]]

# 5 order
c[4].STATUS = 1
c[5].STATUS = 1
m.solve(disp=False)
p5 = [c[5].value[0], c[4].value[0], c[3].value[0],
      c[2].value[0], c[1].value[0], c[0].value[0]]

# plot fit
plt.plot(xm, ym, 'ro', markersize=5)
xp = np.linspace(0, xm.max(), 50)
y2 = 34.6 - 6.23 * xp
plt.plot(xp, y2)
plt.plot((0, 6.5), (30, 30), 'k:')
plt.plot((6.5, 6.5), (30, 0), 'k:')
# plt.plot(xp, np.polyval(p1, xp), 'b--', linewidth=2)
# plt.plot(xp, np.polyval(p2, xp), 'k--', linewidth=3)
# plt.plot(xp, np.polyval(p3, xp), 'g--', linewidth=2)
plt.plot(xp, np.polyval(p5, xp), 'k:', linewidth=2)
# plt.legend(['Data', 'Linear', 'Quadratic', 'Cubic'], loc='best')
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html
# plt.legend(['Data', '3rd', '5th'], loc='best')
plt.xlabel('Napětí[V]')
plt.ylabel('Proud[A]')
plt.grid(True)
plt.axis([0, 1.1 * np.max(xm), 0, 1.1 * np.max(ym)])
plt.minorticks_on()
# plt.box(on=None)
plt.savefig('myfig.png', dpi=300)
plt.show()
print('finished')
