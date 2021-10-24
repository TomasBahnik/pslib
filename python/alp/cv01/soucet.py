a = int(input())
k = int(input())

sum = 0

for i in range(1, a + 1, 1):
    sum += i ** k

print(sum)
