f = open('cisla.txt', 'r')

line = f.readline()
print('Line', line, end='!')

#zapsano stejne jako na tabuli, ale stejne nefunguje.

#priklad fce strip
f = open('cisla.txt', 'r')
for line in f:
    line = line.strip()
    print(line)
    a = int(line)
    print('a=', a, a+10)