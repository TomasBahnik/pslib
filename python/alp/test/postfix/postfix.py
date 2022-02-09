import sys

pole = []
f = open(sys.argv[1], "r")
arg1 = f.read()
for line in arg1:
    pole.append(line.strip())

endword = input()

print(arg1)
print(endword)

# for i in arg1:
#     if endword in arg1:
#         pole.append(i[arg1])

print(pole)
sys.exit(0)
