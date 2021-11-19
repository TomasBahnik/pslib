# pole_1 = [0, 1, 2, 3]
# pole_1 = [5, 6, 7, 8, 9, 10, 11]
pole_1 = [2, 0, 1]
pole_2 = []


# for d in range(0, len(pole_1)):
def inv(x, d):
    if d > x:
        return inv
    else:
        inv(x, d + 1)
        pole_2.append(pole_1[d])


inv(len(pole_1) - 1, 0)

print("k poly {} je inverzni pole {}".format(pole_1, pole_2))
# print(len(pole_1))
