import sys

import numpy as np
from numpy import linalg as la

DEBUG_PRINTS = True


def det_eigenvalues(matrix):
    det = la.det(matrix)
    ev = la.eig(matrix)
    if DEBUG_PRINTS:
        print('\nmatrix\n{}\n'.format(matrix))
        print('\ndeterminant={}'.format(det))
        print('eigen values={}'.format(ev[0]))
        print('right eigen vectors\n{}'.format(ev[1]))


if __name__ == '__main__':
    f = sys.argv[1]
    m_diag = np.diag((1, 2, 3))
    det_eigenvalues(m_diag)
    matrix = np.loadtxt(f)
    det_eigenvalues(matrix)
    sys.exit(0)
