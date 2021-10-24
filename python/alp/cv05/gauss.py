def pm(m):
    for r in range(len(m)):
        for s in range(len(m[0])):
            print(m[r][s], end=" ")
        print()


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


def gauss(m):
    R = len(m)
    S = len(m[0])
    for k in range(R):
        maxVal = m[r][k]
        maxIdx = r
        for r in range(k, r):
            if m[r][k] > maxVal:
                maxVal = m[r][k]
                maxIdx = r
        m[k], m[maxIdx] = m[maxIdx], m[k]

        for r in range(k + 1, R):
            beta = - m[k][k] / m[r][k]
            for s in range(k, S):
                m[r][s] = beta * m[r][s] + m[k][s]
        print("k=", k)
        pm(m)


a = [[1, 1, 1, 3], [2, 1, 8, 11], [-1, -1, 6, 4]]
gauss(a)
