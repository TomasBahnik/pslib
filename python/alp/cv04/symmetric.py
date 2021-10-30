def is_seq_symmetric(sequence):
    if len(sequence) == 0:  # empty list is not symmetric
        return False
    for i in range(1, len(sequence) // 2 + 1):
        # print("{} != {} : {}".format(current[i - 1], current[-i], current[i - 1] != current[-i]))
        if sequence[i - 1] != sequence[-i]:
            return False
    return True


def symmetric_sub_seq(sequence):
    seq_length = 0
    seq_sum = -1
    seq_idx = -1
    for i in range(0, len(sequence) + 1):
        l_s = len(sequence)  # sequence is modified by poping last item at the end
        if l_s == 0:  # when sequence is empty print the last values = output
            print(seq_idx, seq_length)  # tisk navratove hodnoty NEMAZAT
            return
        for j in range(0, l_s):
            sub_seq = sequence[j:l_s]
            # print("{}:{} sub sequence {}".format(j, l_s, sub_seq))
            if is_seq_symmetric(sub_seq):
                # print("symmetric sub sequence : {}".format(sub_seq))
                cur_length = len(sub_seq)
                cur_sum = sum(sub_seq)
                if cur_length > seq_length:
                    seq_idx = j
                    # print("length increased {} -> {} index = {}".format(seq_length, cur_length, seq_idx))
                    seq_length = cur_length
                    seq_sum = cur_sum
                if cur_length == seq_length and cur_sum > seq_sum:
                    seq_idx = j
                    # print("sum increased {} -> {}. index = {}".format(seq_sum, cur_sum, seq_idx))
                    seq_sum = cur_sum
        sequence.pop()


pole = list(map(int, input().split()))
symmetric_sub_seq(pole)
