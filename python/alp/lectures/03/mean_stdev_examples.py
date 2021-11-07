# Příklady pro přednášku "Pole" předmětu Algoritmy a programování
# Jan Kybic, 2016

import math


def mean(v):
    """Calculate a mean of a vector"""
    s = 0.
    for i in range(len(v)):
        s += v[i]
    return (s / len(v))


def stdev(v):
    """Calculate a corrected sample standard deviation"""
    m = mean(v)
    s = 0.
    for i in range(len(v)):
        s += (v[i] - m) ** 2
    return math.sqrt(s / (len(v) - 1))


# pole čísel 0..1000  
a = list(range(1001))
# vypočítáme průměr
print(mean(a))
# vypočítáme směrodatnou odchylku
print(stdev(a))


def mean2(v):
    """Calculate a mean of a vector"""
    s = 0.
    for x in v:
        s += x
    return (s / len(v))


def stdev2(v):
    """Calculate a corrected sample standard deviation"""
    m = mean(v)
    s = 0.
    for x in v:
        s += (x - m) ** 2
    return math.sqrt(s / (len(v) - 1))


# vypočítáme průměr
print(mean2(a))
# vypočítáme směrodatnou odchylku
print(stdev2(a))


def mean3(v):
    """Calculate a mean of a vector"""
    return (sum(v) / len(v))


def stdev3(v):
    """Calculate a corrected sample standard deviation"""
    m = mean(v)
    s = sum([(x - m) ** 2 for x in v])
    return math.sqrt(s / (len(v) - 1))


def stdev4(v):
    """Calculate a corrected sample standard deviation"""
    return math.sqrt(sum([(x - mean(v)) ** 2 for x in v]) / (len(v) - 1))


# vypočítáme průměr
print(mean3(a))
# vypočítáme směrodatnou odchylku
print(stdev3(a))
print(stdev4(a))
