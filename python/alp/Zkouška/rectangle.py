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
red_x = []
red_y = []
for i in range(len(vstup)):
    if vstup[i][2] == 0:
        red_points.append(vstup[i][:2])
        red_x.append(vstup[i][:1])
        red_y.append(vstup[i][1:2])
print(red_points)
print(red_y)

green_points = []
for i in range(len(vstup)):
    if vstup[i][2] == 1:
        green_points.append(vstup[i][:2])


# print(green_points)

# print(red_x[0][0])
def rectangle(x, y):
    x_line = []
    y_line = []
    rec = []
    for i in range(0, len(red_points) - 1):
        if x[i][0] < x[i + 1][0]:
            min_s = x[i][0]
            max_s = x[i+1][0]
        if y[i][0] < y[i + 1][0]:
            min_r = y[i][0]
            max_r = y[i + 1][0]
        for j in range(min_s, max_s):
            for k in range(y[i][0] - y[i + 1][0]):
                rec.append(k)
                print(rec)
            # x_line.append(x[i][0] - x[i + 1][0])
            # y_line.append(y[i][0] - y[i + 1][0])
        # else:
        #     x_line.append(x[i + 1][0] - x[i][0])
        #     y_line.append(y[i + 1][0] - y[i][0])
        #
    # for i in x_line:


if __name__ == '__main__':
    load_input(sys.argv[1])
    # load_char_matrix(sys.argv[1])
    rectangle(red_x, red_y)
