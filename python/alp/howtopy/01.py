"""
def sequence(n):
    while n != 1:
        print(n, end=", ")
        if n % 2 == 0:  # n je sudé
            n = n // 2
        else:
            n = n *3 + 1


sequence(6)

"""
"""
# Výběr slov se sudým pořadím

slova = ["Copak", "je", "to", "za", "fešáka", "?"]

i = 0
delka = len(slova)
while i < delka:
    if i % 2 == 1:
        print(slova[i], end=", ")
    i += 1

"""

"""

def fceA():
    print("volani fceA")


def fceB():
    print("volani fceB")


def fceC():
    print("volani fceC")


def if_case(choice):
    if choice == "a":
        fceA()
    elif choice == "b":
        fceB()
    elif choice == "c":
        fceC()
    else:
        print("Chyba")


if_case("b")

"""

