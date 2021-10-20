# nums = list(map(int, input().split()))
import sys

from common.functions import prime

# nums = [20, -7, -7, -2, 0, 1, 3, 5, 5, 10]


nums = [149, 439, 457, 509, 521, 541, -109, -101, 20, -7, -7, -2, 0, 1, 3, 5, 5, 10, 23,
        37, 271, 4, 3, 11, 541, 67, 79, 83, 433, 227, 137, 149, 439, 457, 509]


def is_seq_interrupted(current, previous):
    if previous is None:
        return True
    d = prime(previous) and not prime(current)
    if d:  # not prime
        return True
    if current < previous:  # decreasing
        return True
    return False


def add_seq(ss, s, sus, les):
    if len(ss) == 0 or len(s) >= len(ss[-1]):
        ss += [s]
        sus += [sum(s)]
        les += [len(s)]


sums = []
lengths = []
seq = []  # empty array/list
seqs = []
seq += [nums[0]]  # start at leftmost element => for cycle below starts at 1 not 0
# find longest non-decreasing AND not interrupted sequence
for i in range(1, len(nums)):
    # p (previous) is None for empty sequence
    p = seq[-1] if len(seq) > 0 else None
    c = nums[i]
    if is_seq_interrupted(c, p):
        add_seq(seqs, seq, sums, lengths)
        seq = []
        if prime(c):
            seq += [c]
    # add to already started sequence non-decreasing prime
    if p is not None and c >= p and prime(c):
        seq += [c]
add_seq(seqs, seq, sums, lengths)  # add last seq

max_length = max(lengths)

max_length_idx = []
for i in range(len(lengths)):
    if lengths[i] == max_length:
        max_length_idx += [i]

max_length_seqs = []
for j in max_length_idx:
    max_length_seqs += [seqs[j]]

print("{} longest sequences : {} of length {} ".format(len(max_length_seqs), max_length_seqs, max_length))
print("All sequences : {}".format(seqs))
print("Lengths of all sequences : {}".format(lengths))
print("Sums of all sequences : {}".format(sums))

sys.exit(0)
