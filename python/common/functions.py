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


def is_seq_symmetric_with_next(current, next_element):
    current += [next_element]
    return is_seq_symmetric(current)


def is_seq_symmetric(sequence):
    if len(sequence) == 0:  # empty list is not symmetric
        return False
    for i in range(1, len(sequence) // 2 + 1):
        # print("{} != {} : {}".format(current[i - 1], current[-i], current[i - 1] != current[-i]))
        if sequence[i - 1] != sequence[-i]:
            return False
    return True


def symmetric_sub_seq(sequence):
    for i in range(0, len(sequence) + 1):
        l_s = len(sequence)  # sequence is modified by poping last item at the end
        if l_s == 0:
            return
        for j in range(i, l_s):
            sub_seq = sequence[j:l_s]
            print("{}:{} sub sequence {}".format(j, l_s, sub_seq))
            if is_seq_symmetric(sub_seq):
                print("symmetric sub sequence : {}".format(sub_seq))
                print("(index, lenght, sum) = ({},{},{})".
                      format(j, len(sub_seq), sum(sub_seq)))
        sequence.pop()


def test_gcd(a, b):
    gcd_1 = gcd1(a, b)
    gcd_2 = gcd2(a, b)
    gcd_e = gcd_euclid(a, b)
    print(gcd_1, gcd_2, gcd_e)


def test_symmetric(sequence):
    print('\ninput={}'.format(sequence))
    symmetric_sub_seq(sequence)


if __name__ == '__main__':
    s1 = [10, -1, 7, 78, 53, 78, 7, -1, 10]
    s2 = [12, -16, -7, -18, -5, -3, 2, 8, 9, -14, -18, -9, 11, -7, -3, 4, -10, 4, -3, -7, 11, -12, -14, 5, -11, -7, 7,
          13, 2, 19, 12, 11]
    s3 = [-14, -8, -9, 2, -18, 12, 1, -1, -14, -14, 13, -2, 15]
    s4 = [-4, -12, 17, 18, -8, 7]
    s5 = [2, 2, 2, 2, 2, 2, 2, 2]

    test_symmetric(s2)
    # test_symmetric(s1)
    # test_symmetric(s3)
    # test_symmetric(s4)
    # test_symmetric(s5)

    sys.exit(0)
