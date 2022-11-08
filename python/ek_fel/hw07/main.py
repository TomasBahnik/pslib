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


if __name__ == '__main__':
    f = Path(sys.argv[1])
    i_f = load_input_file(f)
    ops = list_operations(i_f)
    ops_idx = operations_idx(input_file=i_f, operations=ops)
    m_data = matrix_data(input_file=i_f, op_indexes=ops_idx)
    assert len(ops_idx) == len(m_data) - 1
    validate_matrix_data(matrix_data=m_data)
    np_m_d = np_matrix_data(matrix_data=m_data)
    all_ops = ops + ['']
    print(f"ops: {all_ops}")
    expression: List[Tuple[np.ndarray, str]] = list(zip(np_m_d, all_ops))
    ops_prior = [OP_SIGN_PRIOR for o in ops if OP_SIGN_PRIOR[0] == o]
    operation_sign_priority: List[Tuple[str, int]] = [o_s_p for o in ops for o_s_p in OP_SIGN_PRIOR if o_s_p[0] == o]
    executed = False
    stop = len(operation_sign_priority)
    result = []
    for i in range(stop):
        curr_o_p: int = operation_sign_priority[i][1]
        curr_o_s: str = operation_sign_priority[i][0]
        max_remaining_priorities = max([x[1] for x in operation_sign_priority[i:]])
        # typer.echo(f"{i} : {curr_o_s} priority {curr_o_p}")
        if curr_o_p < max_remaining_priorities:
            if executed:
                result = [curr_o_s, f"m{i + 1}"]
                print(f"save({result} shape {np_m_d[i + 1].shape}")
            else:
                result = [curr_o_s]
                print(f"save({result})")
            executed = False
        elif i < stop - 1:
            result = [f'm{i}', curr_o_s, f'm{i + 1}']
            if curr_o_s == MULTIPLY:
                np_r = np.matmul(np_m_d[i], np_m_d[i + 1])
                print(f"exec+save({result}) shape {np_r.shape}")
            else:
                print(f"exec+save({result})")
            executed = True
        else:
            result = [curr_o_s, f'm{i + 1}']
            print(f"save({result}) shape {np_m_d[i + 1].shape}")
    result = np.matmul(np_m_d[0], np_m_d[1]) - np_m_d[2] + np.matmul(np_m_d[3], np_m_d[4]) + np_m_d[5]
    print(f"\n{result.shape}")
    print(f"{result}")
