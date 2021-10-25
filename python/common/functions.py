import sys


def sum_seq(power, limit):
    ret_val = 0
    if limit >= 0:
        for i in range(0, limit + 1):
            print('{}^{} = {}'.format(i, power, i ** power))
            ret_val += i ** power
    else:  # a < 0
        for i in range(limit, 1):
            print('{}^{} = {}'.format(i, power, i ** power))
            ret_val += i ** power
    return ret_val


# https://cw.fel.cvut.cz/wiki/courses/b3b33alp/cviceni/kratka_videa/c03
# 0 and 1 are not primes
def prime(a):
    a = abs(a)
    if a in [0, 1]:
        return False
    r = True
    for d in range(2, round(a ** 0.5) + 1):
        if a % d == 0:
            r = False
            break
    return r


# first 100 primes
PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
              349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
              467, 479, 487, 491, 499, 503, 509, 521, 523, 541]


def is_num_prime(x):
    """ Decides if the abs(x) is prime number based on presence in first 100 primes. """
    if abs(x) in PRIMES_100:
        return True
    else:
        return False


# https://cw.fel.cvut.cz/wiki/courses/b3b33alp/cviceni/t03
def gcd1(a, b):
    s = 0
    while a != b:
        # print("gcd1 {}".format(s))
        # s += 1
        if a > b:
            a = a - b
        else:
            b = b - a
    return a  # a == b


def gcd2(a, b):
    s = 0
    while b != 0:
        # print("gcd2 {}".format(s))
        # s += 1
        t = b
        b = a % b
        a = t
    return a


# Euclid algorithm see introcs/gcd/readme.md
def gcd_euclid(a, b):
    if b == 0:
        return a
    return gcd_euclid(b, a % b)


nums = [20, -7, -7, -2, 0, 1, 3, 5, 5, 10]


def test_primes(numbers):
    for n in numbers:
        v1 = is_num_prime(n)
        v2 = prime(n)
        if not (v1 == v2):
            print("{} : {} vs {}".format(n, v1, v2))


def is_seq_symmetric(current, next_element):
    current += [next_element]
    for i in range(1, len(current) // 2 + 1):
        print("{} != {} : {}".format(current[i - 1], current[-i], current[i - 1] != current[-i]))
        if current[i - 1] != current[-i]:
            return False
    return True


def test_gcd(a, b):
    gcd_1 = gcd1(a, b)
    gcd_2 = gcd2(a, b)
    gcd_e = gcd_euclid(a, b)
    print(gcd_1, gcd_2, gcd_e)


def test_symmetric(sequence, a):
    print(is_seq_symmetric(sequence, a))


if __name__ == '__main__':
    s = [10, -1, 7, 78, 53, 78, 7, -1]
    print(is_seq_symmetric(s, 11))
    s = [10, 8, 2, 5, 8]
    print(is_seq_symmetric(s, 10))
    s = [10, 5, -4, 20, -4, 5]
    print(is_seq_symmetric(s, 10))
    s = [3, 6, 6]
    print(is_seq_symmetric(s, 3))
    sys.exit(0)
