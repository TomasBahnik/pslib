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


def np_matrix_data(matrix_data: List[List[str]]) -> List[np.ndarray]:
    ret: List[np.ndarray] = []
    for m_d in matrix_data:
        m_rows = m_d[1:]
        m_array = [list(map(int, row.split())) for row in m_rows]
        np_array = np.array(m_array, dtype=int)
        # print(f"matrix array shape:{np_array.shape}, matrix dims : {m_d[0]}")
        ret.append(np.array(np_array, dtype=int))
    return ret


def operations_idx(input_file: List[str], operations: List[str]) -> List[int]:
    op_indexes: List[int] = []
    start_idx: int = 0
    # no Value error - all operations are in input file
    for op in operations:
        start_idx = input_file.index(op, start_idx)
        op_indexes.append(start_idx)
    return op_indexes


def process_ops(operation_sign_priority, data: List[np.ndarray]):
    stop = len(operation_sign_priority)
    new_ops = []
    new_data = []
    current_priorities = set([x[1] for x in operation_sign_priority])
    if len(current_priorities) == 1:
        # all priorities are the same we can proceed from left to right
        np_r = data[0]
        for i in range(stop):
            current_op_sign: str = operation_sign_priority[i][0]
            # if current_op_sign == MULTIPLY:
            #     np_r = np.matmul(data[i], data[i + 1])
            if current_op_sign == SUBTRACT:
                np_r = np_r - data[i + 1]
            if current_op_sign == ADD:
                np_r = np_r + data[i + 1]
        return [], [np_r]

    for i in range(stop):
        current_op_priority: int = operation_sign_priority[i][1]
        next_op_priority: int = operation_sign_priority[i + 1][1] if i < stop - 1 else None
        same_priority: bool = current_op_priority == next_op_priority
        current_op_sign: str = operation_sign_priority[i][0]
        current_priorities = ([x[1] for x in operation_sign_priority])
        max_remaining_priorities = max([x[1] for x in operation_sign_priority[i:]])
        if current_op_priority < max_remaining_priorities:
            # if the next operation priority =  current_op_priority  add also f'm{i + 1}'
            res = [current_op_sign, i + 1] if same_priority else [current_op_sign]
            new_ops.append(current_op_sign)
            if same_priority:
                new_data.append(data[i + 1])
                print(f"save({res} shape {data[i + 1].shape}")
            else:
                print(f"save({res} no data appended")
        elif i < stop - 1:  # not last operation and curr_o_p >= max_remaining_priorities
            res = [i, current_op_sign, i + 1]
            np_r = None
            if current_op_sign == MULTIPLY:
                np_r = np.matmul(data[i], data[i + 1])
                print(f"{i} {MULTIPLY} {i + 1} shape {np_r.shape}")
                new_data.append(np_r)
            if current_op_sign == SUBTRACT:
                np_r = data[i] - data[i + 1]
                print(f"{i} {SUBTRACT} {i + 1} shape {np_r.shape}")
                new_data.append(np_r)
            if current_op_sign == ADD:
                np_r = data[i] + data[i + 1]
                print(f"{i} {ADD} {i + 1} shape {np_r.shape}")
                new_data.append(np_r)
            else:
                print(f"save({res})")
        else:  # current = last operation
            res = [current_op_sign, i + 1]
            new_ops.append(current_op_sign)
            new_data.append(data[i + 1])
            print(f"save({res}) shape {data[i + 1].shape}")
    return new_ops, new_data


if __name__ == '__main__':
    f = Path(sys.argv[1])
    i_f = load_input_file(f)
    ops = list_operations(i_f)
    ops_idx = operations_idx(input_file=i_f, operations=ops)
    m_data = matrix_data(input_file=i_f, op_indexes=ops_idx)
    assert len(ops_idx) == len(m_data) - 1
    validate_matrix_data(matrix_data=m_data)
    np_m_d: List[np.ndarray] = np_matrix_data(matrix_data=m_data)
    expected_result = np.matmul(np_m_d[0], np_m_d[1]) - np_m_d[2] + np.matmul(np_m_d[3], np_m_d[4]) + np_m_d[5]
    ops_prior = [OP_SIGN_PRIOR for o in ops if OP_SIGN_PRIOR[0] == o]
    op_sign_priority: List[Tuple[str, int]] = [o_s_p for o in ops for o_s_p in OP_SIGN_PRIOR if o_s_p[0] == o]
    ops, np_m_d = process_ops(op_sign_priority, np_m_d)
    print(f"1st paas: {ops}")
    op_sign_priority: List[Tuple[str, int]] = [o_s_p for o in ops for o_s_p in OP_SIGN_PRIOR if o_s_p[0] == o]
    ops, np_m_d = process_ops(op_sign_priority, np_m_d)
    print(f"2nd paas: {ops}")
    if len(np_m_d) == 1:
        result = np_m_d[0]
        print(f"result: {result}")
        print(f"expected_result : {expected_result}")
        print(f"expected_result == result  : {expected_result == result}")
