import sys

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

    def columns(self) -> list[list[int]]:
        """Return columns of the matrix.

        Each row has the same length as the 1st row in original matrix.
        """
        return [[row[i] for row in self.matrix] for i in range(len(self.matrix[0]))]


if __name__ == "__main__":
    p = Piskvorky(sys.argv[1])
    for row_idx, row in enumerate(p.rows()):
        winning_col_idx = sub_seq_of_length(sequence=row, length=5)
        if winning_col_idx is not None:
            print(f"Winning position : row {row_idx}, column: {winning_col_idx}")
    for col_idx, col in enumerate(p.columns(), start=0):
        winning_row_idx = sub_seq_of_length(sequence=col, length=5)
        if winning_row_idx is not None:
            print(f"Winning position : row {winning_row_idx}, column: {col_idx}")
