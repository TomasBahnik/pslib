def fce0():
    class X:
        pass

    f = None
    for i in range(1000):
        g = X()
        g.a = f
        g.b = i
        f = g

    for i in range(100):
        f = f.a
    print(f.b)


def fce1():
    for i in range(4):
        for j in range(i, 4):
            print(j, end="")
        print()


def fce2():
    data = [4, 4, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8]
    count = 0
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count = count + 1
            print("adding{}".format(i))
    print(count)


def fce3(n):
    x = 1400
    count = 0
    while count < x:
        for i in range(70):
            j = 0
            while j < 90:
                if j > n:
                # xyz(x)
                    count += count
                j += 1
    print(count)

if __name__ == "__main__":
    fce3(10)
