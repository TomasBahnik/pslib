import sys
import operator

empty = 0
cross = 1
circle = 2
# how many solution is enough
enough_num_of_solutions = 1
# num_of_solutions <= enough_num_of_solutions
num_of_solutions = 0


def load_matrix(file) -> list[list[int]]:
    """Load 2D array from file"""
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.split())))
    return pole


def last_cross_missing(sequence: list[int]) -> bool:
    s = sum(sequence)
    cnt_empty = sequence.count(empty)
    cnt_cross = sequence.count(cross)
    # len must be 5 = 4 crosses (1) and 1 empty (0) and sum must be 4
    # search all sub-sequences of length 5
    if s != 4:
        return False
    if cnt_empty == 1 and cnt_cross == 4:
        return True
    else:
        return False


def sub_seq_of_length(sequence, length):
    """Check sub-sequences of given length for winning condition."""
    l_s = len(sequence)
    if l_s < length:  # l_s - length < 0
        # print("ERROR length of sequence < = length. Length = {}, seq length={}".format(length, l_s))
        return
    for j in range(0, l_s - length + 1):  # j <= l_s - length
        sub_seq = sequence[j:j + length]
        if last_cross_missing(sub_seq):
            # add j because we need empty idx counted from the original sequence
            empty_idx = sub_seq.index(empty) + j
            # print("{} : cross at {} in {} wins! piskvorka = {} ".format(sys.argv[1], empty_idx, sequence, sub_seq))
            return empty_idx


class Piskvorky:
    def __init__(self, file_with_matrix):
        self.matrix = load_matrix(file_with_matrix)

    def rows(self) -> list[list[int]]:
        return self.matrix

    def row_length(self):
        return len(self.matrix[0])

    def columns(self) -> list[list[int]]:
        """Return columns of the matrix.

        Each row has the same length as the 1st row in original matrix.
        """
        return [[row[i] for row in self.matrix] for i in range(self.row_length())]

    def col_length(self) -> int:
        """All columns have the same length"""
        return len(self.columns()[0])

    def shift_up(self):
        """Difference of indexes is equal and can be negative zero (main diag) or positive"""
        return range(-self.row_length() + 1, self.row_length()), operator.sub

    def shift_down(self):
        """Sum of indexes is constant"""
        return range(0, 2 * self.row_length() - 1), operator.add

    def diagonals(self, shift_range_operator):
        """Return diagonal indexes of each shift """
        d_r, op = shift_range_operator
        ret = {}
        for shift in d_r:
            diag_idx = [self.matrix[i][j] for i in range(self.row_length()) for j
                        in range(self.row_length()) if (op(i, j)) == shift]
            ret[shift] = diag_idx
        filter_elements = {key: value for key, value in ret.items() if len(value) > 4}
        return filter_elements


def check_win(elements, rows: bool):
    for idx, values in enumerate(elements):
        winning_idx = sub_seq_of_length(sequence=values, length=5)
        if winning_idx:
            print(f"Winning position : {idx}, {winning_idx}") if rows else \
                print(f"Winning position : {winning_idx}, {idx}")


if __name__ == "__main__":
    p = Piskvorky(sys.argv[1])
    check_win(p.rows(), rows=True)
    check_win(p.columns(), rows=False)
    down_diag = p.diagonals(shift_range_operator=p.shift_down())
    up_diag = p.diagonals(shift_range_operator=p.shift_up())
    print("End")
