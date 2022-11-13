import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np


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


def apply_op(operation: str, operand_1: int, operand_2: int) -> int:
    """ used for integer based operations"""
    match operation:
        case '+':
            return operand_1 + operand_2
        case '-':
            return operand_1 - operand_2
        case '*':
            return operand_1 * operand_2
        case _:
            print("unknown operation")


def apply_op_nd(operation: str, operand_1: np.ndarray, operand_2: np.ndarray) -> np.ndarray:
    """ used for matrix based operations. matrix is represented as multidimensional (nd) array"""
    match operation:
        case '+':
            return operand_1 + operand_2
        case '-':
            return operand_1 - operand_2
        case '*':
            # matmul = matrix multiplication
            return np.matmul(operand_1, operand_2)
        case _:
            print("unknown operation")


def sign_priority(operations: List[str]) -> List[Tuple[str, int]]:
    return [o_s_p for o in operations for o_s_p in OP_SIGN_PRIOR if o_s_p[0] == o]


def apply_max_priority_op(tmp: int, operations: List[str], operands: List[int], max_priority_idx: int):
    curr_max_idx = max_priority_idx
    curr_ops = operations[curr_max_idx]
    tmp = apply_op(operation=curr_ops, operand_1=tmp, operand_2=operands[curr_max_idx + 1])
    # check how far is next max priority idx
    # if 1 apply again if > 1 update next_data and next_ops
    return tmp


def apply_max_priority_op_np(tmp: np.ndarray, operations: List[str],
                             operands: List[np.ndarray], max_priority_idx: int) -> np.ndarray:
    curr_max_idx = max_priority_idx
    curr_ops = operations[curr_max_idx]
    tmp = apply_op_nd(operation=curr_ops, operand_1=tmp, operand_2=operands[curr_max_idx + 1])
    # check how far is next max priority idx
    # if 1 apply again if > 1 update next_data and next_ops
    return tmp


def printable_expression(operations: List[str], operands: List[int]):
    for i in range(len(operands) - 1):
        # 10 + 18 * 5 * 8 - 21 * 6
        print(f'{operands[i]} {operations[i]} ', end='')
    print(operands[-1])


ADD = '+'
SUBTRACT = '-'
MULTIPLY = '*'

OPERATIONS = [ADD, SUBTRACT, MULTIPLY]
OPERATIONS_PRIORITY = [0, 0, 1]
OP_SIGN_PRIOR = list(zip(OPERATIONS, OPERATIONS_PRIORITY))


def process_expression(operations: List[str], operands: List[np.ndarray]) -> Tuple[List[str], List[np.ndarray]]:
    """ Process expression from left to right. Operations are processed in ordered of decreasing priorities.
        Operation priorities are set by constants above
    """
    s_p = sign_priority(operations)
    priorities = np.array([p[1] for p in s_p])
    max_priority = max(priorities)
    # find positions of max priority operations
    max_priority_indexes = np.where(priorities == max_priority)[0]
    first_max_idx = max_priority_indexes[0]
    # add all operations and operands preceding first_max_idx
    new_operands = operands[:first_max_idx]
    new_ops = operations[:first_max_idx]
    # first operand of current max priority operation
    tmp = operands[first_max_idx]
    for i in range(len(max_priority_indexes)):
        curr_max_idx = max_priority_indexes[i]
        tmp = apply_max_priority_op_np(tmp=tmp, operations=operations, operands=operands,
                                       max_priority_idx=curr_max_idx)
        # check how far is next max priority idx
        # if 1 apply again if > 1 update next_data and next_ops
        next_max_idx = max_priority_indexes[i + 1] if i + 1 < len(max_priority_indexes) else curr_max_idx
        delta_idx = next_max_idx - curr_max_idx
        last_max_idx = curr_max_idx == max_priority_indexes[-1]
        if delta_idx == 1:
            continue
        else:
            new_operands.append(tmp)
            # if it is the last max priority operation add everything
            # else add all only up to the next priority position
            append_operands = operands[curr_max_idx + 2:] if last_max_idx \
                else operands[curr_max_idx + 2:next_max_idx]
            new_operands = new_operands + append_operands

            append_operations = operations[curr_max_idx + 1:] if last_max_idx \
                else operations[curr_max_idx + 1:next_max_idx]
            new_ops = new_ops + append_operations
            # prepare for next calculation of max priority expression
            tmp = operands[next_max_idx]
    # expression is DONE. Only 1 operand remains and NO operations
    # RETURN results
    if len(new_operands) == 1:
        return new_ops, new_operands
    # We have to recursively return the results to parent function calls
    # so the first call to process_expression can return it to the main
    return process_expression(operations=new_ops, operands=new_operands)


def matrix_expression():
    f = Path(sys.argv[1])
    i_f = load_input_file(f)
    ops, ops_idx = op_sign_idx(input_file=i_f)
    matrices = matrix_data(input_file=i_f, op_indexes=ops_idx)
    assert len(ops_idx) == len(matrices) - 1
    last_operations, last_operands = process_expression(operations=ops, operands=matrices)
    result = last_operands[0]
    print(f"{result.shape}\n{result}")


# 34 * 10 + 18 * 5 * 8 - 21 * 6 * 5 = 430
TEST_OPS: List[str] = [MULTIPLY, ADD, MULTIPLY, MULTIPLY, SUBTRACT, MULTIPLY, MULTIPLY]
TEST_DATA = [34, 10, 18, 5, 8, 21, 6, 5]
RESULT = 430


# 34 * 10 - 18 + 5 * 8 + 21 = 383
# TEST_OPS: List[str] = [MULTIPLY, SUBTRACT, ADD, MULTIPLY, ADD]
# TEST_DATA = [34, 10, 18, 5, 8, 21]
# RESULT = 383

def int_expression():
    assert len(TEST_OPS) == len(TEST_DATA) - 1
    printable_expression(operations=TEST_OPS, operands=TEST_DATA)
    last_operations, last_operands = process_expression(operations=TEST_OPS, operands=TEST_DATA)
    print(f"expected no operations left = {last_operations}")
    assert len(last_operations) == 0
    print(f"expected {RESULT} = {last_operands[0]}")
    assert last_operands[0] == RESULT


if __name__ == '__main__':
    matrix_expression()
