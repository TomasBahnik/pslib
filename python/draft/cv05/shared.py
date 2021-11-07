def load_matrix(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.split())))
    return pole


def column(matrix, i):
    return [row[i] for row in matrix]