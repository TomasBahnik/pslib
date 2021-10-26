
x = [0]*(len(m[0])-1)
for k in range (len(m) - 1, -1, -1):
    s = 0
    for i in range(k+1, len(m[0])-1):
        s += m[k][i]*x[i]


# prace s polem
def f(a):
    # a[0] = "ahoj"
    # a.append = "ahoj"
    # a.pop()
    a = [0, 0, 0, 0]
    print("f:", a)


b = [1, 2, 3, 4]
f(b)
print(b)


# deepcopy use
import copy

a = [[1, 2, 3], [4, 5, 6]]
b = copy.deepcopy(a)
print(b)
