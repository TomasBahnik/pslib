# def perm(text, out):
#     if len(text) == 0:
#         print(out)
#     # print("text=", text, "out=", out)
#     for i in range(len(text)):
#         rest = text[:i] + text[i + 1:]
#         perm(rest, out + text[i])


# perm("Tomas", "")

# fce moje range
# def myRange(n):
#     i = 0
#     while i < n:
#         yield i  # nezacne zezhora
#         i += 1


def perm(text, out):
    if len(text) == 0:
        yield out
    # print("text=", text, "out=", out)
    for i in range(len(text)):
        rest = text[:i] + text[i + 1:]
        perms = perm(rest, out + [text[i]])
        for p in perms:
            yield p


for p in perm([1, 2, 3, 4], []):
    print(p)

# print(allPerms)
# for p in allPerms:
#     a, b, c = p
#     if a + b > 10:
#         print(p)
