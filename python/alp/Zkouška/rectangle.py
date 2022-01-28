import sys
RED = 0
GREEN = 1

def load_lines_matrix(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.rstrip().split())))
    print(pole)
    return pole


# def load_char_matrix(file):
#     pole = []
#     with open(file, 'r') as f:
#         for line in f:
#             chars = [char for char in line.rstrip()]
#             pole.append(chars)
#     print(pole)
#     return pole




if __name__ == '__main__':
    load_lines_matrix(sys.argv[1])
    # load_char_matrix(sys.argv[1])
