import random
import sys
import time

import matplotlib.pyplot as plt


def sequential_search(a, q):
    """ Returns 'True' if 'a' contains 'q' """
    for x in a:
        if x == q:
            return True
    return False


def binary_search(a, q):
    """ Returns 'True' if 'a' contains 'q'. 'a' must be non-decreasing. """
    l = 0  # first index of the subinterval
    h = len(a) - 1  # last index of the subinterval
    while l <= h:
        m = (l + h) // 2  # middle point
        if a[m] == q:
            return True
        if a[m] > q:
            h = m - 1
        else:
            l = m + 1
    return False


def time_sequential_search(n):
    nrep = 100  # počet opakování
    a = [random.randrange(2 ** 30) for i in range(n)]  # n náhodných čísel
    tottimein = 0.  # součet časů
    tottimenotin = 0.  # součet časů
    tottimebin = 0.  # součet časů
    tottimebnotin = 0.  # součet časů
    for i in range(nrep):
        q = -1  # určitě tam není
        # r=sequential_search(a,q)
        t0 = time.perf_counter()
        r = sequential_search(a, q)
        tottimenotin += time.perf_counter() - t0
        assert (not r)
        t0 = time.perf_counter()
        r = q in a
        tottimebnotin += time.perf_counter() - t0
        q = a[random.randrange(n)]
        # r=sequential_search(a,q)
        t0 = time.perf_counter()
        r = sequential_search(a, q)
        tottimein += time.perf_counter() - t0
        assert (r)
        t0 = time.perf_counter()
        r = q in a
        tottimebin += time.perf_counter() - t0

    tottimein /= nrep
    tottimenotin /= nrep
    tottimebin /= nrep
    tottimebnotin /= nrep
    return tottimein, tottimenotin, tottimebin, tottimebnotin


def time_binary_search(n):
    nrep = 100  # počet opakování
    tottimein = 0.  # součet časů
    tottimenotin = 0.  # součet časů
    for i in range(nrep):
        a = [random.randrange(2 ** 30) for i in range(n)]  # n náhodných čísel
        a.sort()
        q = -1  # určitě tam není
        t0 = time.perf_counter()
        for i in range(nrep):
            r = binary_search(a, q)
        tottimenotin += time.perf_counter() - t0
        assert (not r)
        q = a[random.randrange(n)]
        t0 = time.perf_counter()
        for i in range(nrep):
            r = binary_search(a, q)
        tottimein += time.perf_counter() - t0
        assert (r)

    tottimein /= nrep * nrep
    tottimenotin /= nrep * nrep
    return tottimein, tottimenotin


def time_and_plot_seq_search():
    ns = [1000, 3000, 10000, 30000, 100000, 300000, 600000, 1000000, 2000000, 3000000]
    # ns=[1000,3000,10000]
    plt.figure(1)
    timein = []
    timenotin = []
    timebin = []
    timebnotin = []
    for n in ns:
        print("n=", n)
        tin, tnotin, tbin, tbnotin = time_sequential_search(n)
        timein += [tin]
        timenotin += [tnotin]
        timebin += [tbin]
        timebnotin += [tbnotin]
    plt.plot(ns, timein, marker='o', color='b', linestyle='-', linewidth=3, label='seq in')
    plt.plot(ns, timenotin, marker='o', color='g', linestyle='-', linewidth=3, label='seq not in')
    plt.plot(ns, timebin, marker='o', color='b', linestyle='--', linewidth=1, label='Python in')
    plt.plot(ns, timebnotin, marker='o', color='g', linestyle='--', linewidth=1, label='Python not in')
    plt.xlabel('n')
    plt.ylabel('time [s]')
    plt.legend(loc='upper left')
    plt.savefig("seq_search_time_log.pdf")
    plt.show()


def time_and_plot_bin_search():
    ns = [1000, 3000, 10000, 30000, 100000, 300000, 600000, 1000000, 2000000, 3000000]
    # ns=[1000,3000,10000]
    timein = []
    timenotin = []
    timebin = []
    timebnotin = []
    for n in ns:
        print("n=", n)
        tin, tnotin, tbuiltinin, tbuiltinnotin = time_sequential_search(n)
        tbin, tbnotin = time_binary_search(n)
        timein += [tin]
        timenotin += [tnotin]
        timebin += [tbin]
        timebnotin += [tbnotin]
    plt.figure(1)
    plt.loglog(ns, timein, marker='o', color='b', linestyle='-', linewidth=3, label='seq in')
    plt.loglog(ns, timenotin, marker='o', color='g', linestyle='-', linewidth=3, label='seq not in')
    plt.loglog(ns, timebin, marker='o', color='r', linestyle='-', linewidth=3, label='binary in')
    plt.loglog(ns, timebnotin, marker='o', color='m', linestyle='-', linewidth=3, label='binary not in')
    plt.xlabel('n')
    plt.ylabel('time [s]')
    plt.legend(loc='upper left')
    plt.savefig("binseq_search_time.pdf")
    plt.figure(2)
    plt.plot(ns, timebin, marker='o', color='r', linestyle='-', linewidth=3, label='binary in')
    plt.plot(ns, timebnotin, marker='o', color='m', linestyle='-', linewidth=3, label='binary not in')
    plt.xlabel('n')
    plt.ylabel('time [s]')
    plt.legend(loc='upper left')
    plt.savefig("bin_search_time.pdf")
    plt.show()


if __name__ == "__main__":
    # time_and_plot_seq_search()
    time_and_plot_bin_search()
    sys.exit(0)
