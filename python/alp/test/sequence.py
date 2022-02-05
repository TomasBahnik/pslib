"""
    VSTUPY
1) 20 2 -2 -10
---> 1 0
     1 2

2) 20 2 -2 -10 6 -3 4 -9
---> 1 0
     4 3

3) 20 20 20 20 20
---> 0 0
     0 5

4) 20 -20 20 -40 20
---> 0 3
     -1 0


"""
import sys


x = list(map(int, input().split()))
avg = sum(x) / len(x)


# print(prumer)
def dist_from_avg(input_seq):
    prumer = sum(input_seq) / len(input_seq)
    return [abs(p - prumer) for p in input_seq]


def nejblizsi(distances):
    return distances.index(min(distances))


def nevzdalenejsi(distances):
    return distances.index(max(distances))


def nejdelsi_pod_posloupnst(distances, max_dist):
    l_d = len(distances)
    max_l = 0
    rets = []
    for j in range(l_d):
        for k in range(l_d - j):
            sub_seq = distances[j:l_d - k]
            if max(sub_seq) < max_dist:
                if len(sub_seq) > max_l:
                    rets = (j, len(sub_seq))
                    max_l = len(sub_seq)
    if len(rets) > 0:
        print(rets[0], rets[1])
    else:
        print(-1, 0)


def test(sequence):
    dist = dist_from_avg(sequence)
    print(nejblizsi(dist), nevzdalenejsi(dist))
    nejdelsi_pod_posloupnst(dist, 10)


def minimum(x):
    min = float("inf")
    min_idx = None
    for i in range(len(x)):
        if abs(x[i] - avg) < min:
            min_idx = i
            min = abs(x[i] - avg)
    # print(min_idx)
    return min_idx


def maximum(x):
    max = 0
    max_idx = 0
    for i in range(len(x)):
        if abs(x[i] - avg) > max:
            max_idx = i
            max = abs(x[i] - avg)
    # print(max_idx)
    return max_idx


def seq(x):
    global longest
    len1 = []
    len2 = []
    for i in range(len(x)):
        if abs(x[i] - avg) < 10:
            len1.append(x[i])
        else:
            len2 = len1
            len1 = []
        if len(len2) > len(len1):
            longest = len2
        else:
            longest = len1
    return longest


def seq_idx(seq):
    count = 0
    if len(seq) == 0:
        count = -1
    else:
        first_val = seq[0]
        for val in x:
            if val == first_val:
                break
            else:
                count += 1
    return count


if __name__ == '__main__':
    # vstup = list(map(int, input().split()))
    # test(vstup)
    print(minimum(x), maximum(x))
    print(seq_idx(seq(x)), len(seq(x)))
    sys.exit(0)
