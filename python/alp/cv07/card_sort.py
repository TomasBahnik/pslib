order = {}
# order = {"2":1, "3":2 ...}
order["2"] = 1
order["3"] = 2
order["4"] = 3
order["5"] = 4
order["6"] = 5
order["7"] = 6
order["8"] = 7
order["9"] = 8
order["10"] = 9
order["J"] = 10
order["Q"] = 11
order["K"] = 12
order["A"] = 13


def card_sort(a):
    for i in range(len(a) - 1):
        for j in range(i + 1, len(a)):
            bi, hi = a[i]  # bi=prvni_prvek_z_a, hi=druhy_prvek_z_a
            bj, hj = a[j]
            if (bi > bj) or ((bi == bj) and order[hi] > order[hj]):  # and hi == hj):
                a[i], a[j] = a[j], a[i]


cards = [[0, 'Q'], [2, '10'], [1, 'K'],
         [1, '8'], [2, '10'], [2, '4'],
         [3, '4'], [0, '4'], [1, '3'],
         [2, '5'], [0, 'K'], [3, '4'],
         [1, 'J'], [0, '3'], [0, '9']]
card_sort(cards)
print(cards)
