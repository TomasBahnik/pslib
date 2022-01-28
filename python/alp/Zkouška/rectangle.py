import sys

RED = 0
GREEN = 1


def load_input(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.rstrip().split())))
    # print(pole)
    return pole


vstup = load_input(sys.argv[1])
red_points = []
for i in range(len(vstup)):
    if vstup[i][2] == 0:
        red_points.append(vstup[i][:2])
print(red_points)

green_points = []
for i in range(len(vstup)):
    if vstup[i][2] == 1:
        green_points.append(vstup[i][:2])
print(green_points)



if __name__ == '__main__':
    load_input(sys.argv[1])
    # load_char_matrix(sys.argv[1])
