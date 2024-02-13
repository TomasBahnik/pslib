import operator
import sys
from dataclasses import dataclass

EMPTY = 0
CROSS = 1
CIRCLE = 2
# how many solution is enough
enough_num_of_solutions = 1
# num_of_solutions <= enough_num_of_solutions
num_of_solutions = 0
INTS_2D = list[list[int]]


def load_matrix(file) -> INTS_2D:
    """Load 2D array from file"""
    pole = []
    with open(file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            pole.append(list(map(int, line.split())))
    return pole


def last_cross_missing(sequence: list[int]) -> bool:
    s = sum(sequence)
    cnt_empty = sequence.count(EMPTY)
    cnt_cross = sequence.count(CROSS)
    # len must be 5 = 4 crosses (1) and 1 empty (0) and sum must be 4
    # search all sub-sequences of length 5
    if s != 4:
        return False
    if cnt_empty == 1 and cnt_cross == 4:
        return True
    else:
        return False


@dataclass(frozen=True)
class Orthogonal:
    """Column or row"""
    coords: list[tuple[int, int]]
    values: list[int]

    def check_lengths(self):
        assert len(self.coords) == len(self.values)

    def filter_length(self, min_length: int) -> bool:
        """Only values with len > min_length"""
        return len(self.values) > min_length

    def sub_seq_of_length(self, length: int) -> int | None:
        """Check all sub-sequences of given length for winning condition."""
        l_s: int = len(self.values)
        if l_s < length:  # l_s - length < 0
            return None
        for j in range(0, l_s - length + 1):  # j <= l_s - length
            sub_seq: list[int] = self.values[j:j + length]
            if last_cross_missing(sub_seq):
                # add j because we need empty idx counted from the original sequence
                winning_idx: int = sub_seq.index(EMPTY) + j
                return winning_idx
        return None

    def check_win(self):
        winning_idx = self.sub_seq_of_length(length=5)
        # explicitly check for None because bool(0) = False
        if winning_idx is not None:
            print(f"Winning position : {self.coords[winning_idx]}")


@dataclass(frozen=True)
class Diagonal(Orthogonal):
    """Diagonal - sum or diff of indexes is fixed"""
    shift: int


class Piskvorky:
    def __init__(self, file_with_matrix):
        self.matrix = load_matrix(file_with_matrix)

    def rows(self) -> INTS_2D:
        return self.matrix

    def row_length(self):
        return len(self.matrix[0])

    def columns(self) -> INTS_2D:
        """Return columns of the matrix.

        Each row has the same length as the 1st row in original matrix.
        """
        return [[row[i] for row in self.matrix] for i in range(self.row_length())]

    def col_length(self) -> int:
        """All columns have the same length"""
        return len(self.columns()[0])

    def diagonal_up(self):
        """Difference of indexes is equal and can be negative zero (main diag) or positive"""
        return range(-self.row_length() + 1, self.row_length()), operator.sub

    def diagonal_down(self):
        """Sum of indexes is constant"""
        return range(0, 2 * self.row_length() - 1), operator.add

    def orthogonal(self) -> list[Orthogonal]:
        """List of rows and columns"""
        rows_coords = [[(i, j) for j in range(self.row_length())] for i in range(self.row_length())]
        cols_coords = [[(j, i) for j in range(self.row_length())] for i in range(self.row_length())]
        rows_values: INTS_2D = self.rows()
        cols_values: INTS_2D = self.columns()
        rows: list[Orthogonal] = [Orthogonal(coords=coords, values=values)
                                  for coords, values in zip(rows_coords, rows_values)]
        columns: list[Orthogonal] = [Orthogonal(coords=coords, values=values)
                                     for coords, values in zip(cols_coords, cols_values)]
        return rows + columns

    def diagonals(self, diagonal_range_operator) -> list[Diagonal]:
        """List of all diagonals."""
        d_r, op = diagonal_range_operator
        diagonals: list[Diagonal] = []
        for shift in d_r:
            coords = [(i, j) for i in range(self.row_length()) for j
                      in range(self.row_length()) if (op(i, j)) == shift]
            values = [self.matrix[i][j] for i in range(self.row_length()) for j
                      in range(self.row_length()) if (op(i, j)) == shift]
            diagonal: Diagonal = Diagonal(shift=shift, coords=coords, values=values)
            diagonals.append(diagonal)
        filter_diagonals = [diag for diag in diagonals if diag.filter_length(min_length=4)]
        return filter_diagonals


if __name__ == "__main__":
    p = Piskvorky(sys.argv[1])
    for o in p.orthogonal():
        o.check_win()
    for dd in p.diagonals(diagonal_range_operator=p.diagonal_down()):
        dd.check_win()
    for ud in p.diagonals(diagonal_range_operator=p.diagonal_up()):
        ud.check_win()
    print("End")
