import sys

passes = [1, 2, 3, 4, 5, 6, 7]
pattern = [[1, 6, 4, 6, 2, 6, 4, 6],
           [7, 7, 7, 7, 7, 7, 7, 7],
           [5, 6, 5, 6, 5, 6, 5, 6],
           [7, 7, 7, 7, 7, 7, 7, 7],
           [3, 6, 4, 6, 3, 6, 4, 6],
           [7, 7, 7, 7, 7, 7, 7, 7],
           [5, 6, 5, 6, 5, 6, 5, 6],
           [7, 7, 7, 7, 7, 7, 7, 7]]
# 1/16
input_1 = [[24, 24],
           [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]

# 1/4
input_2 = [[24, 8],
           [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]
input_3 = [[24, 8],
           [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0,
            0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

image_3_orig = [[0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def empty_image(w, h):
    b = []
    for i in range(h):
        b.append([0] * w)
    return b


DEBUG_PRINTS = True


def debug_print(message, print_debug):
    if print_debug:
        print(message)


def num_of_samples_in_pass(p):
    x = 0
    for r in pattern:
        x += r.count(p)
    return x


def img_pass(i, p):
    img_w = i[0][0]
    img_h = i[0][1]
    img_sample = i[1]
    img_size = img_w * img_h
    num_of_patterns = (img_w // len(pattern[0])) * (img_h // len(pattern[0]))
    samples_in_pass = num_of_samples_in_pass(p) * num_of_patterns
    debug_print("{}x{} : {} new samples_in_pass {}".format(img_w, img_h, samples_in_pass, p), DEBUG_PRINTS)
    return samples_in_pass


def idx_of_pass(p):
    x = []
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            if pattern[i][j] == p:
                x += [[i, j]]
    return x


idx_of_passes = {}
for p in passes:
    idx_of_passes[p] = idx_of_pass(p)

pass_ratio = {2 ** 6: 1, 2 ** 5: 2, 2 ** 4: 3, 2 ** 3: 4, 2 ** 2: 5, 2 ** 1: 6, 2 ** 0: 7}


def test2(i):
    img_w = i[0][0]
    img_h = i[0][1]
    e_i = empty_image(img_w, img_h)
    img_size = img_w * img_h
    img_coded = i[1]
    num_of_patterns = (img_w // len(pattern[0])) * (img_h // len(pattern[0]))
    power_of_2 = img_size // len(img_coded)
    max_pass = pass_ratio[power_of_2]
    w_r = img_w // 8
    r_r = img_h // 8
    row_range = [x * 8 for x in range(0, r_r)]
    col_range = [x * 8 for x in range(0, w_r)]
    all_samples = []
    for p in range(1, max_pass + 1):
        samples = idx_of_passes[p]
        for r in row_range:
            for c in col_range:
                for s in samples:
                    n_r = s[0] + r
                    n_c = s[1] + c
                    all_samples += [[n_r, n_c]]
    decode = [all_samples, img_coded]
    # sorted_list = sorted(list, key=lambda x: (x[0], -x[1]))
    all_samples.sort(key=lambda x: (x[0], x[1]))
    if len(all_samples) != len(img_coded):
        print("ERROR - coded length mismatch exiting")
        sys.exit(1)
    for i in range(len(img_coded)):
        val = img_coded[i]
        coord = all_samples[i]
        e_i[coord[0]][coord[1]] = val
    print(e_i)


def test_decode(input_data, orig_image):
    zeroes = input_data.count(0)
    ones = input_data.count(1)
    img_zeroes = 0
    img_ones = 0
    for r in orig_image:
        img_zeroes += r.count(0)
        img_ones += r.count(1)
    if zeroes != img_zeroes or ones != img_ones:
        print("ERROR : pocty nul a jednicek jsou ruzne")
    else:
        print("pocty nul a jednicek jsou stejne")


def test_adam(img_w, img_h):
    e_i = empty_image(img_w, img_h)
    w_r = img_w // 8
    r_r = img_h // 8
    row_range = [x * 8 for x in range(0, r_r)]
    col_range = [x * 8 for x in range(0, w_r)]
    all_samples = []
    pruchody = []
    for p in range(1, 8):
        samples = idx_of_passes[p]
        for r in row_range:
            for c in col_range:
                for s in samples:
                    n_r = s[0] + r
                    n_c = s[1] + c
                    pruchody.append(p)
                    all_samples += [[n_r, n_c]]
    # all_samples.sort(key=lambda x: (x[0], x[1]))
    if len(all_samples) != len(pruchody):
        print("ERROR - length mismatch exiting")
        sys.exit(1)
    for i in range(len(all_samples)):
        coord = all_samples[i]
        pruchod = pruchody[i]
        e_i[coord[0]][coord[1]] = pruchod
    print(e_i)


def test(i):
    tot = 0
    img_w = i[0][0]
    img_h = i[0][1]
    e_i = empty_image(img_w, img_h)
    img_size = img_w * img_h
    img_sample = i[1]
    samples = {}
    idx_pass = {}
    prev = 0
    for p in range(1, 8):
        s = img_pass(i, p)
        tot += s
        debug_print("total samples_in_pass {}: {}, fraction {}".format(p, tot, img_size // tot), DEBUG_PRINTS)
        samples[p] = img_sample[prev:tot]
        prev = tot

    w_r = img_w // 8
    r_r = img_h // 8
    # [0, 8, 16]
    row_range = [x * 8 for x in range(0, r_r)]
    col_range = [x * 8 for x in range(0, w_r)]
    for pruchod in passes:
        sam = samples[pruchod]
        pos_pruchod = idx_of_passes[pruchod]
        if len(sam) > 0 and len(pos_pruchod) > 0:
            for r, c in pos_pruchod:
                for f in row_range:
                    for g in col_range:
                        e_i[r + f][c + g] = sam.pop(0)
    print(e_i)


if __name__ == "__main__":
    # test_adam(24, 8)
    test_decode(input_3[1], image_3_orig)
    # test2(input_3)
