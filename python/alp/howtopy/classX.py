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