cnt = 0
n = 50
for i in range(70):
    j = i
    while j > 0:
        if j < n:
            cnt += 1
        j -= 1
    print("{} : {}".format(i, cnt))

print(cnt)
