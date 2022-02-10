import sys

import numpy as np

RED = 0
GREEN = 1


def load_input(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.rstrip().split())))
    # print(pole)
    return pole


def red_points_areas(all_points, red_points):
    """
    Kazde dvojici cervenych bodu prirad plochu. index je z pozice vsech bodu
    :param all_points
    :param red_points
    :return: [[idx_1, idx_2], area] sorted by area descending
    """
    ret_val = []
    for r_p_1 in red_points:
        idx_1 = all_points.index(r_p_1)
        for r_p_2 in red_points:
            idx_2 = all_points.index(r_p_2)
            if idx_1 < idx_2:  # only different points and do not include 2x
                x_1 = r_p_1[0]
                x_2 = r_p_2[0]
                y_1 = r_p_1[1]
                y_2 = r_p_2[1]
                area = abs(x_2 - x_1) * abs(y_2 - y_1)
                ret_val.append([[idx_1, idx_2], area])
    ret_val.sort(key=lambda x: x[1], reverse=True)
    return ret_val


def is_point_in_rectangle(point, rectangles, all_points):
    for rectangle in rectangles:
        r1_idx = rectangle[0][0]
        r2_idx = rectangle[0][1]
        x1 = all_points[r1_idx][0]
        y1 = all_points[r1_idx][1]
        x2 = all_points[r2_idx][0]
        y2 = all_points[r2_idx][1]
        px = point[0]
        py = point[1]
        ret_val = x1 <= px <= x2 and y1 <= py <= y2
        print("point {} in rectangle {}? : {}".format(point, [x1, y1, x2, y2], ret_val))


# def split_red_green():
#     red_x = []
#     red_y = []
#     for i in range(len(all_points)):
#         if all_points[i][2] == 0:
#             red_points.append(all_points[i][:2])
#             red_x.append(all_points[i][:1])
#             red_y.append(all_points[i][1:2])
#     print(red_points)
#     print(red_y)


# green_points = []
# for i in range(len(all_points)):
#     if all_points[i][2] == 1:
#         green_points.append(all_points[i][:2])
# print(green_points)
# print(red_x[0][0])
# def rectangle(x, y):
#     min_s = []
#     min_r = []
#     max_s = []
#     max_r = []
#     rec = []
#     for i in range(0, len(red_points) - 1):
#         if x[i][0] < x[i + 1][0]:
#             min_s.append([i][0])
#             max_s.append(x[i+1][0])
#         if y[i][0] < y[i + 1][0]:
#             min_r.append(y[i][0])
#             max_r.append(y[i + 1][0])
#             for j in range(len(min_s), len(max_s)):
#                 for k in range(len(min_r), len(max_r)):
#                     rec.append(k)
#                     print(rec)


# x_line.append(x[i][0] - x[i + 1][0])
# y_line.append(y[i][0] - y[i + 1][0])
# else:
#     x_line.append(x[i + 1][0] - x[i][0])
#     y_line.append(y[i + 1][0] - y[i][0])
#
# for i in x_line:
def test_2(file):
    print(file)
    all_points = load_input(file)
    green_points = [x for x in all_points if x[2] == GREEN]
    red_points = [x for x in all_points if x[2] == RED]
    rectangles = red_points_areas(all_points, red_points)
    for g_p in green_points:
        is_point_in_rectangle(g_p, rectangles, all_points)


def test(file):
    print(file)
    all_points = load_input(file)
    green_points = [x for x in all_points if x[2] == GREEN]
    if len(green_points) == 0:
        print("NONE")
        return
    red_points = [x for x in all_points if x[2] == RED]
    if len(red_points) < 2:
        print("NONE")
        return
    # numpy version
    # all_points_np = np.zeros((len(all_points), len(all_points)), dtype=int)
    areas = red_points_areas(all_points, red_points)
    print(areas[0][0])


files = ['easy_1023.txt', 'easy_2072.txt', 'easy_2970.txt', 'easy_4705.txt', 'easy_5718.txt',
         'easy_7408.txt', 'easy_8274.txt', 'easy_9216.txt']

reseni = ['1 3', 'NONE', '2 12', '10 15', '18 41', 'NONE', '0 60', 'NONE']

if __name__ == '__main__':
    test_2('easy_1023.txt')
    # for i in range(len(files)):
    #     test(files[i])
    #     print('reseni : {}\n'.format(reseni[i]))
    sys.exit(0)
