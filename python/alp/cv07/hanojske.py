def move(n, source, dest, temp):
    if n > 0:
        move(n - 1, source, temp, dest)
        # presun posledni z source na dest
        t = source.pop()
        dest.append(t)
        # dest.append(source.pop())
        print("a =", a, "b =", b, "c =", c)
        move(n - 1, temp, dest, source)


a = [3, 2, 1]
b = []
c = []
print("a =", a, "b =", b, "c =", c)
move(len(a), a, c, b)
print("a =", a, "b =", b, "c =", c)
