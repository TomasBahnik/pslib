from alp.common.funkce import sym


# from alp.common.funkce import poslup


def poslup(pole):
    delka = 1
    for i in range(0, len(pole) + 1):
        l_p = len(pole)
        if l_p == 0:
            return
        for j in range(i, l_p):
            pod_pole = pole[j:l_p]
            # print(i)
            if sym(pod_pole):
                for p in range(0, len(pod_pole) + 1):
                    n = 0
                    if p > n:
                        n = p
                        if delka < n:
                            delka = n
                            if p == len(pod_pole):
                                print(j, delka)

        pole.pop()


# pro načtení a převedení vstupu na pole celých čísel můžete použít příkaz
# https://cw.fel.cvut.cz/wiki/courses/b3b33alp/cviceni/t01
s3 = list(map(int, input().split()))
# s3 = [-14, -8, -9, 2, -18, 12, 1, -1, -14, -14, 13, -2, 15]
poslup(s3)
# s3 = [14, 2, 14]

# def test_sym():
#     x = []
#     print("vstup {}: je symetricka {}".format(x, sym(x)))
#     x = [1, 2, 3, 5, 9, 89, 45, 85, 5, 105, 68, 1]
#     print("vstup {}: je symetricka {}".format(x, sym(x)))
#     s1 = [10, -1, 7, 78, 53, 78, 7, -1, 10]
#     print("vstup {}: je symetricka {}".format(s1, sym(s1)))
#     s2 = [12, -16, -7, -18, -5, -3, 2, 8, 9, -14, -18, -9, 11, -7, -3, 4, -10, 4, -3, -7, 11, -12, -14, 5, -11, -7, 7,
#           13, 2, 19, 12, 11]
#     s3 = [-14, -8, -9, 2, -18, 12, 1, -1, -14, -14, 13, -2, 15]
#     s4 = [-4, -12, 17, 18, -8, 7]
#     s5 = [2, 2, 2, 2, 2, 2, 2, 2]
#     s6 = [10, 8, 2, 5, 8, 10]
#     print("vstup {}: je symetricka {}".format(s6, sym(s6)))

# print('\ninput={}, length={}'.format(s2, len(s2)))
# symmetric_sub_seq(s2)
