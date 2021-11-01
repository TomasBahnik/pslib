# cnt = 0
# global cnt
# cnt += 1
# print(cnt)
# f(a)


# def f(a):
#     if a >= 10:
#         return
#     print(a)
#     f(a + 1)
# f(1)

# vypocet faktorialu
def fakt(n):
    if n == 0 or n == 1:
        return 1
    return n * fakt(n - 1)


print(fakt(5))
