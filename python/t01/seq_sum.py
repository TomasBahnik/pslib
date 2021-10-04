# nums = list(map(int, input().split()))
import sys

nums = [20, -7, -7, -2, 0, 1, 3, 5, 5, 10]

PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
              349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
              467, 479, 487, 491, 499, 503, 509, 521, 523, 541]


def is_prime_100(x):
    return x in PRIMES_100


# keep only absolute value primes in original array
# TODO keep track of non primes - interrupted sequences
def filter_primes(a):
    r = []
    for n in a:
        if is_prime_100(abs(n)):
            r += [n]
    return r


nums_primes = filter_primes(nums)

seq = []
seq += [nums_primes[0]]
seqs = []
# find longest non-decreasing AND not interrupted sequence
# keep only primes so we do not need check for them
for i in range(1, len(nums_primes)):
    if nums_primes[i] < nums_primes[i - 1]:  # decreasing
        del seq[i - 1]
    else:  # non decreasing >=
        seq += [nums_primes[i]]
print(seq)
sys.exit(0)
