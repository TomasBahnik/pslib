# Find longest symmetric sequences of integers.
# In case of of two such sequences select the one with larger sum
# Case of the same length and sum is not covered in assignment. This implementation  selects
# the one with highest index.
# Output = the pair (index, length) of the sequence
import sys

from common.functions import symmetric_sub_seq

# test sequences
s1 = [10, -1, 7, 78, 53, 78, 7, -1, 10]
expected_output_1 = (0, 9)

# example inputs and outputs from HW04
# https://cw.fel.cvut.cz/wiki/courses/b3b33alp/cviceni/t04
s2 = [12, -16, -7, -18, -5, -3, 2, 8, 9, -14, -18, -9, 11, -7, -3, 4, -10, 4, -3, -7, 11, -12, -14, 5, -11, -7, 7,
      13, 2, 19, 12, 11]
expected_output_2 = (12, 9)

s3 = [-14, -8, -9, 2, -18, 12, 1, -1, -14, -14, 13, -2, 15]
expected_output_3 = (8, 2)

s4 = [-4, -12, 17, 18, -8, 7]
expected_output_4 = (3, 1)

s5 = [2, 2, 2, 2, 2, 2, 2, 2]
expected_output_5 = (0, 8)
# end of example inputs and outputs from HW04

# special sequences
s6 = [22, 32, 4, 452, -1, -123, 2, 2]
expected_output_6 = (6, 2)

s7 = [22, 32, 4, 452, 123, 1, 2, 52]
expected_output_7 = (3, 1)

s8 = [2122, 32, 4, 452, 123, 1, 2, 52]
expected_output_8 = (0, 1)

s9 = [2122, 32, 4, 452, 123, 1, 1, 2, 34452]
expected_output_9 = (5, 2)

# ambiguous output (0,4) or (9 4) or (15, 4) equal length and sum
s10 = [2122, 1, 2, 2, 1, 32, 4, 452, 123, 1, 1, 2, 2, 1, 34452, 2, 1, 1, 2]
expected_output_10 = (0, 4, 10, 4, 15, 4)


def test_symmetric(sequence, output):
    print('\ninput={}\nlength={}'.format(sequence, len(sequence)))
    symmetric_sub_seq(sequence)
    print('expected output={}'.format(output))


if __name__ == '__main__':
    test_symmetric(s1, expected_output_1)
    test_symmetric(s2, expected_output_2)
    test_symmetric(s3, expected_output_3)
    test_symmetric(s4, expected_output_4)
    test_symmetric(s5, expected_output_5)
    test_symmetric(s6, expected_output_6)
    test_symmetric(s7, expected_output_7)
    test_symmetric(s8, expected_output_8)
    test_symmetric(s9, expected_output_9)
    test_symmetric(s10, expected_output_10)
    sys.exit(0)
