#matice cislo 1

def pm(m):
    for r in range(len(m)):
        for s in range(len(m[0])):
            print(m[r][s], end=" ")
        print()
#
#
# a = [[1, 2, 3], [3, 4, 5], [0, 6, 1]]
# pm(a)
# print(a)

#matice cislo 2

# def mv(m, v):
#     res = [0] * len(m)
#     for r in range(len(m)):
#         for i in range(len(v)):
#             res[r] = m[r][i] * v[i]
#     return res
#
#
# a = [[1, 2, 3], [3, 4, 5], [0, 6, 1]]
# v = [1, 1, 1]
# print(mv(a, v))


def mm(m1, m2):
    R = len(m1)
    S = len(m2[0])
    res = []
    for r in range(R):
        res.append([])
        for s in range(S):
            res[r].append(0)
    for r in range(R):
        for s in range(S):
            for i in range(len(m2)):
                res[r][s] += m1[r][i] * m2[i][s]
    return res


a = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
pm(mm(a,a))