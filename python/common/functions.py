def sum_seq(power, limit):
    ret_val = 0
    if limit >= 0:
        for i in range(0, limit + 1):
            print('{}^{} = {}'.format(i, power, i ** power))
            ret_val += i ** power
    else:  # a < 0
        for i in range(limit, 1):
            print('{}^{} = {}'.format(i, power, i ** power))
            ret_val += i ** power
    return ret_val
