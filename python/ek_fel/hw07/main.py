import sys
from pathlib import Path
from typing import List

from numpy import linalg as la

DEBUG_PRINTS = True


def det_eigenvalues(matrix):
    det = la.det(matrix)
    ev = la.eig(matrix)
    if DEBUG_PRINTS:
        print('\nmatrix\n{}\n'.format(matrix))
        print('\ndeterminant={}'.format(det))
        # print('eigenvalues={}'.format(ev[0]))
        # print('right eigenvectors\n{}'.format(ev[1]))


ADD = '+'
SUBTRACT = '-'
MULTIPLY = '*'

OPERATIONS = [ADD, SUBTRACT, MULTIPLY]


class MatrixExpression:
    def __init__(self, dims, data, operation=None):
        self.m_expression = (dims, data, operation)


def load_input_file(file: Path) -> List[str]:
    """ dims, data, operation """
    m_expressions: List[MatrixExpression]
    with open(file, mode='r') as input_file:
        return [line.strip() for line in input_file.readlines()]


def list_operations(input_file: List[str]) -> List[str]:
    ret = [line.strip() for line in input_file if line.strip() in OPERATIONS]
    return ret


def matrix_data(input_file: List[str], op_indexes: List[int]):
    m_data: List[List[str]] = []
    start_idx: int = 0
    for o_i in op_indexes:
        m_d = input_file[start_idx:o_i]
        m_data.append(m_d)
        start_idx = o_i + 1
    last_m_data = input_file[start_idx:]
    m_data.append(last_m_data)
    return m_data


def validate_matrix_data(matrix_data: List[List[str]]):
    for m_d in matrix_data:
        m_dims = list(map(int, m_d[0].split()))
        assert len(m_dims) == 2
        rows: int = m_dims[0]
        cols: int = m_dims[1]
        m_rows = m_d[1:]
        assert rows == len(m_rows)
        for row_str in m_rows:
            row_items = list(map(int, row_str.split()))
            assert len(row_items) == cols


def operations_idx(input_file: List[str], operations: List[str]) -> List[int]:
    op_indexes: List[int] = []
    start_idx: int = 0
    # no Value error - all operations are in input file
    for op in operations:
        start_idx = input_file.index(op, start_idx)
        op_indexes.append(start_idx)
    return op_indexes


if __name__ == '__main__':
    f = Path(sys.argv[1])
    i_f = load_input_file(f)
    ops = list_operations(i_f)
    ops_idx = operations_idx(input_file=i_f, operations=ops)
    m_data = matrix_data(input_file=i_f, op_indexes=ops_idx)
    validate_matrix_data(matrix_data=m_data)
    print(f"ops: {ops} length of ops : {len(ops)}")
    print(f"ops_idx: {ops_idx} length of ops_idx : {len(ops_idx)}")
    print(f"length of matrix data : {len(m_data)}")
    # m_diag = np.diag((1, 2, 3))
    # det_eigenvalues(m_diag)
    # m1 = np.loadtxt(f)
    # m1.transpose()
    # det_eigenvalues(m1.transpose())
    # sys.exit(0)
