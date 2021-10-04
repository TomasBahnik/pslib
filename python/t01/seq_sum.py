# nums = list(map(int, input().split()))
import sys

nums = [149, 439, 457, 509, 521, -109, -101, 20, -7, -7, -2, 0, 1, 3, 5, 5, 10, 23, 37, 271, 4, 3, 11, 541, 67, 79,
        83, 433, 227, 137, 149, 439, 457, 509]

PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
              349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
              467, 479, 487, 491, 499, 503, 509, 521, 523, 541]


def is_prime_100(x):
    if abs(x) in PRIMES_100:
        return True
    else:
        return False


def seq_is_interrupted(current, previous):
    if previous is None:
        return True
    d = is_prime_100(previous) and not is_prime_100(current)
    if d:  # not prime
        return True
    if current < previous:  # decreasing
        return True
    return False


def add_seq(ss, s):
    if len(ss) == 0 or len(s) >= len(ss[-1]):
        ss += [s]


seq = [] # empty array/list
seqs = []
seq += [nums[0]] # start at leftmost element => for cycle below starts at 1 not 0
# find longest non-decreasing AND not interrupted sequence
for i in range(1, len(nums)):
    p = seq[-1] if len(seq) > 0 else None
    c = nums[i]
    if seq_is_interrupted(c, p):
        add_seq(seqs, seq)
        seq = []
        if is_prime_100(c):
            seq += [c]
    if p is not None and c >= p and is_prime_100(c):  # non-decreasing
        seq += [c]
add_seq(seqs, seq)  # add last seq
print(seqs)
sys.exit(0)
