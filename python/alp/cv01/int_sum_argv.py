import sys

#
# soucet mocnin posloupnosti cisel
# example
#   python int_sum_argv.py 2 5
#
# output
#
# k = 2, a = 5
# 0^2 = 0
# 1^2 = 1
# 2^2 = 4
# 3^2 = 9
# 4^2 = 16
# 5^2 = 25
# sum i^2 : i \in <0,5> = 55
#

# k-ta mocnina : prvni argument
k = int(sys.argv[1])

# druhy argument
# a >= 0 : soucet od 0 do a (vcetne)
# a < 0 : soucet od a do 0 (vcetne)
a = int(sys.argv[2])
print('k = {}, a = {}'.format(k, a))

total_sum = 0
if a >= 0:
    for i in range(0, a + 1):  # start incl , stop excl
        total_sum += i ** k
        print('step {}: {}^{} = {}: total sum = {}'.format(i, i, k, i ** k, total_sum))
else:  # a < 0
    for i in range(a, 1):
        print('{}^{} = {}'.format(i, k, i ** k))
        total_sum += i ** k

print('sum i^{} : i \\in <{},{}> = {}'.format(k, 0, a, total_sum))
sys.exit(0)
