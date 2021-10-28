def sym(pole):
    if len(pole) == 0:
        return False
    for i in range(0, len(pole) // 2):
        if pole[i] != pole[- (1 + i)]:
            # print("{} != {}".format(i, -(i + 1)))
            # print("{} != {}".format(pole[i], pole[-(i + 1)]))
            return False
        # print("index {} = {}".format(i, -(i + 1)))
        # print("hodnota {} = {}".format(pole[i], pole[-(i + 1)]))
    return True


# test

x = []
print("vstup {}: je symetricka {}".format(x, sym(x)))
x = [1, 2, 3, 5, 9, 89, 45, 85, 5, 105, 68, 1]
print("vstup {}: je symetricka {}".format(x, sym(x)))
s1 = [10, -1, 7, 78, 53, 78, 7, -1, 10]
print("vstup {}: je symetricka {}".format(s1, sym(s1)))
s2 = [12, -16, -7, -18, -5, -3, 2, 8, 9, -14, -18, -9, 11, -7, -3, 4, -10, 4, -3, -7, 11, -12, -14, 5, -11, -7, 7,
      13, 2, 19, 12, 11]
s3 = [-14, -8, -9, 2, -18, 12, 1, -1, -14, -14, 13, -2, 15]
s4 = [-4, -12, 17, 18, -8, 7]
s5 = [2, 2, 2, 2, 2, 2, 2, 2]
s6 = [10, 8, 2, 5, 8, 10]
print("vstup {}: je symetricka {}".format(s6, sym(s6)))
