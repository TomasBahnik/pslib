def pmul(p1, p2):
    res = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1) + len(p2)):
        for j in range(len(p2)):
            res[i + j] = p1[i] * p2[j]
    return res


a = [10, 0, 3, 1]
b = [1, 2]
pp(pmul(a, b))
