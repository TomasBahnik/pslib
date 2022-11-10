import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np

ADD = '+'
SUBTRACT = '-'
MULTIPLY = '*'

OPERATIONS = [ADD, SUBTRACT, MULTIPLY]
OPERATIONS_PRIORITY = [0, 0, 1]
OP_SIGN_PRIOR = list(zip(OPERATIONS, OPERATIONS_PRIORITY))


def load_input_file(file: Path) -> List[str]:
    with open(file, mode='r') as input_file:
        return [line.strip() for line in input_file.readlines()]


def op_sign_idx(input_file: List[str]):
    signs: List[str] = []
    indexes: List[int] = []
    for i in range(len(input_file)):
        line = input_file[i].strip()
        if line in OPERATIONS:
            signs.append(line)
            indexes.append(i)
    return signs, indexes


def to_int_data(m_data_str: List[List[str]]) -> List[np.ndarray]:
    """ convert string (numerical) matrices to np arrays of type int
        easy to multiply and sum
    """
    ret: List[np.ndarray] = []
    for m_d in m_data_str:
        # skip the row with dimensions
        m_rows = m_d[1:]
        m_array = [list(map(int, row.split())) for row in m_rows]
        np_array = np.array(m_array, dtype=int)
        ret.append(np.array(np_array, dtype=int))
    return ret


def matrix_data(input_file: List[str], op_indexes: List[int]) -> List[np.ndarray]:
    """ reads matrix data from input file
        first line are matrix dimensions rows x cols
        the rest is matrix data
    """
    m_data_str: List[List[str]] = []
    start_idx: int = 0
    for operation_idx in op_indexes:
        # reads all lines related to matrix i.e.
        # 1. row, cols
        # 2 matrix data  = all lines up to next operation
        m_d: List[str] = input_file[start_idx:operation_idx]
        m_data_str.append(m_d)
        # move to index just after next operation
        # i.e.  start of the next matrix
        start_idx = operation_idx + 1
    last_m_data = input_file[start_idx:]
    m_data_str.append(last_m_data)
    validate_matrix_data(m_data_str)
    # convert to int matrices
    m_data_int = to_int_data(m_data_str=m_data_str)
    return m_data_int


def validate_matrix_data(m_data_str: List[List[str]]):
    """ check the dimensions and actual number of rows and cols"""
    for m_d in m_data_str:
        m_dims = list(map(int, m_d[0].split()))
        assert len(m_dims) == 2
        rows: int = m_dims[0]
        cols: int = m_dims[1]
        m_rows = m_d[1:]
        assert rows == len(m_rows)
        for row_str in m_rows:
            row_items = list(map(int, row_str.split()))
            assert len(row_items) == cols


def process_equal_priorities(operation_sign_priority, data: List[np.ndarray]):
    """ there are only equal priorities evaluate expression from left to right
        It is state when all higher priory expression were resolved
        should be used for simple cases with just + and -
    """
    n_operations = len(operation_sign_priority)
    np_r = data[0]
    for i in range(n_operations):
        current_op_sign: str = operation_sign_priority[i][0]
        if current_op_sign == MULTIPLY:
            np_r = np.matmul(data[i], data[i + 1])
        if current_op_sign == SUBTRACT:
            np_r = np_r - data[i + 1]
        if current_op_sign == ADD:
            np_r = np_r + data[i + 1]
    remaining_ops = []
    final_result = [np_r]
    return remaining_ops, final_result


def process_lower_priority(op_idx, new_ops, new_data, current_op_sign, same_priority, data):
    """ if the next operation priority =  current_op_priority  add also next data = i + 1'
        e.g. m1 + m2 -  means we can safely add next expression whatever it is
        but. m1 + m2 *  means we have to evaluate next expression first!!
    """
    new_ops.append(current_op_sign)
    if same_priority:
        new_data.append(data[op_idx + 1])


def process_higher_priority(op_idx, new_data, current_op_sign, data):
    """ not the last operation
        BUT current operation priority >= max_remaining_priorities
    """
    if current_op_sign == MULTIPLY:
        tmp_result = np.matmul(data[op_idx], data[op_idx + 1])
        new_data.append(tmp_result)
    if current_op_sign == SUBTRACT:
        tmp_result = data[op_idx] - data[op_idx + 1]
        new_data.append(tmp_result)
    if current_op_sign == ADD:
        tmp_result = data[op_idx] + data[op_idx + 1]
        new_data.append(tmp_result)


def process_last_operation(op_idx, new_ops, new_data, current_op_sign, data):
    new_ops.append(current_op_sign)
    new_data.append(data[op_idx + 1])


def process_ops(operations, data: List[np.ndarray]):
    operation_sign_priority: List[Tuple[str, int]] = \
        [o_s_p for o in operations for o_s_p in OP_SIGN_PRIOR if o_s_p[0] == o]
    n_operations = len(operation_sign_priority)
    new_ops = []
    new_data = []
    current_priorities = [p[1] for p in operation_sign_priority]
    # set keeps only unique elements
    # i.e. if all are the same just one remains
    if len(set(current_priorities)) == 1:
        return process_equal_priorities(operation_sign_priority, data=data)
    for i in range(n_operations):
        not_last_operation = i < n_operations - 1
        current_op_priority: int = operation_sign_priority[i][1]
        next_op_priority: int = operation_sign_priority[i + 1][1] if not_last_operation else None
        same_priority: bool = current_op_priority == next_op_priority
        current_op_sign: str = operation_sign_priority[i][0]
        max_remaining_priorities = max([x[1] for x in operation_sign_priority[i:]])
        if current_op_priority < max_remaining_priorities:
            process_lower_priority(op_idx=i, new_ops=new_ops, new_data=new_data,
                                   current_op_sign=current_op_sign, same_priority=same_priority, data=data)
        elif not_last_operation:
            process_higher_priority(op_idx=i, new_data=new_data,
                                    current_op_sign=current_op_sign, data=data)
        else:
            process_last_operation(op_idx=i, new_ops=new_ops, new_data=new_data,
                                   current_op_sign=current_op_sign, data=data)
    o, d = process_ops(new_ops, new_data)
    if len(d) == 1:
        # no operations
        assert len(o) == 0
        return d[0]


if __name__ == '__main__':
    f = Path(sys.argv[1])
    i_f = load_input_file(f)
    ops, ops_idx = op_sign_idx(input_file=i_f)
    matrices = matrix_data(input_file=i_f, op_indexes=ops_idx)
    assert len(ops_idx) == len(matrices) - 1
    d = process_ops(ops, matrices)
    print(f"result\n{d}")
    expected_result = np.matmul(matrices[0], matrices[1]) - matrices[2] + np.matmul(matrices[3], matrices[4]) + \
                      matrices[5]
    print(f"expected_result\n{expected_result}")
    print(f"expected_result == result\n{expected_result == d}")
