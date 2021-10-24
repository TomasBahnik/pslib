def psum(p1, p2):
    # res = []
    # for i in range(max(len(p1), len(p2))):
    #     res.append(0)
    res = [0] * max(len(p1), len(p2))
    for s in range(len(res)):
        if s < len(p1):
            res[s] = p1[s]
        if s > len(p2):
            res[s] += p2[s]
    return res


# pp(psum([1, 1, 1], [2, 2, 2]))

