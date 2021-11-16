# Experiments for sorting algorithms

import random
import time

import matplotlib.pyplot as plt


def bubble_sort(a):
    """ sorts array a in-place in ascending order"""
    for i in range(len(a) - 1, 0, -1):
        # i=n-1..1.  a[i+1:] is already sorted
        exchanged = False
        for j in range(i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]  # exchange
                exchanged = True
        if not exchanged: break
    return None


def python_sort(a):
    a.sort()


def selection_sort(a):
    """ sorts array a in-place in ascending order"""
    for i in range(len(a) - 1, 0, -1):
        # find out what should go to a[i]
        max_pos = 0
        for j in range(1, i + 1):
            if a[j] > a[max_pos]:
                max_pos = j
        a[i], a[max_pos] = a[max_pos], a[i]


def insertion_sort(a):
    """ sorts array a in-place in ascending order"""
    for i in range(1, len(a)):  # a[0:i] is sorted
        val = a[i]
        j = i
        while j > 0 and a[j - 1] > val:
            a[j] = a[j - 1]
            j -= 1
        a[j] = val


def test_sort(f=bubble_sort):
    for j in range(100):
        n = 100
        a = [random.randrange(100000) for i in range(n)]
        f(a)
        for i in range(n - 1):
            assert (a[i] <= a[i + 1])
    print(f.__name__, " sort test passed")


def time_sort(n, f, sorted=False):
    nrep = 1
    tottime = 0.
    for i in range(nrep):
        a = [random.randrange(100000) for i in range(n)]
        if sorted:
            a.sort()
        t0 = time.clock()
        f(a)
        tottime += time.clock() - t0
    return tottime / nrep


def time_sorting_algorithms(sorted=False,
                            algs=[bubble_sort, selection_sort, insertion_sort, python_sort],
                            prefix="time_sorting_algorithms",
                            ns=[500, 1000, 2000, 4000, 6000, 8000, 10000]):
    alltimes = []
    for alg in algs:
        algtimes = []
        for n in ns:
            t = time_sort(n, alg, sorted=sorted)
            print("Algorithm ", alg.__name__, " n=", n, " time=", t)
            algtimes += [t]
        alltimes += [algtimes]
    plt.figure(1)
    for i in range(len(algs)):
        plt.plot(ns, alltimes[i], marker='o', linewidth=3, label=algs[i].__name__)
    plt.legend(loc='upper left')
    plt.xlabel('N')
    plt.ylabel('time [s]')
    plt.savefig(prefix + "_sorted.pdf" if sorted else prefix + ".pdf")
    plt.figure(2)
    for i in range(len(algs)):
        plt.loglog(ns, alltimes[i], marker='o', linewidth=3, label=algs[i].__name__)
    plt.legend(loc='upper left')
    plt.xlabel('N')
    plt.ylabel('time [s]')
    plt.savefig(prefix + "_sorted_log.pdf" if sorted else prefix + "_log.pdf")
    plt.show()


if __name__ == "__main__":
    # time_and_plot_seq_search()
    time_sorting_algorithms(sorted=False)
    time_sorting_algorithms(sorted=True)
