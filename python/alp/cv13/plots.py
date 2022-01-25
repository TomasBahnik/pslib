# from mpl_toolkits import mplot3d
import sys

import matplotlib.pyplot as plt
import numpy as np


def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))


def lin_f(x, y):
    return 5 * x ** 2 + 3 * y ** 3


def plot_f():
    x = np.linspace(-6, 6, 10)
    y = np.linspace(-6, 6, 10)
    X, Y = np.meshgrid(x, y)
    Z = lin_f(X, Y)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # ax.contour3D(X, Y, Z, 100, cmap='binary')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    # ax.view_init(40, 5)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    ax.set_title('surface')
    plt.show()


def plot_3d():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # Data for a three-dimensional line
    zline = np.linspace(0, 15, 1000)
    xline = np.sin(zline)
    yline = np.cos(zline)
    ax.plot3D(xline, yline, zline, 'gray')
    # Data for three-dimensional scattered points
    zdata = 15 * np.random.random(100)
    xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
    ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
    plt.show()


def plot_2d():
    x = np.linspace(-5, 5, 100)
    y = (x + 1) * abs(x - 3) + 2
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, 'r')
    plt.show()


if __name__ == '__main__':
    plot_2d()
    sys.exit(0)
