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
    all_rows = []
    for i in range(len(pattern)):
        one_row = []
        for j in range(len(pattern[i])):
            if pattern[i][j] == p:
                one_row += [[i, j]]
        all_rows.append(one_row)
    return all_rows


idx_of_passes = {}
for p in passes:
    idx_of_passes[p] = idx_of_pass(p)

pass_ratio = {2 ** 6: 1, 2 ** 5: 2, 2 ** 4: 3, 2 ** 3: 4, 2 ** 2: 5, 2 ** 1: 6, 2 ** 0: 7}


def column(matrix, i):
    return [row[i] for row in matrix]


def adam7_decode(test_input):
    img_w = test_input[0][0]
    img_h = test_input[0][1]
    e_i = empty_image(img_w, img_h)
    img_coded = test_input[1]
    w_r = img_w // 8
    r_r = img_h // 8
    row_range = [x * 8 for x in range(0, r_r)]
    col_range = [x * 8 for x in range(0, w_r)]
    all_samples = all_image_samples(col_range, row_range)
    if len(all_samples) != len(img_coded):
        print("ERROR - coded length mismatch exiting")
        sys.exit(1)
    for i in range(len(img_coded)):
        val = img_coded[i]
        coord = all_samples[i]
        e_i[coord[0]][coord[1]] = val
    print(e_i)


def all_image_samples(col_range, row_range):
    all_samples = []
    for p in range(1, 8):
        samples = idx_of_passes[p]
        for r in row_range:
            for row_samples in samples:
                for c in col_range:
                    for row_sample in row_samples:
                        n_r = row_sample[0] + r
                        n_c = row_sample[1] + c
                        all_samples += [[n_r, n_c]]
    return all_samples


def adam7_encode(input_data, orig_image):
    zeroes = input_data.count(0)
    ones = input_data.count(1)
    img_zeroes = 0
    img_ones = 0
    for r in orig_image:
        img_zeroes += r.count(0)
        img_ones += r.count(1)
    if zeroes != img_zeroes or ones != img_ones:
        print("ERROR : pocty nul a jednicek jsou ruzne")
        sys.exit(1)
    else:
        print("pocty nul a jednicek jsou stejne")
    img_w = len(orig_image[0])
    img_h = len(column(orig_image, 0))
    w_r = img_w // 8
    r_r = img_h // 8
    row_range = [x * 8 for x in range(0, r_r)]
    col_range = [x * 8 for x in range(0, w_r)]
    all_samples = []
    encoded_image = []
    for p in range(1, 8):
        samples = idx_of_passes[p]
        for r in row_range:
            for row_samples in samples:
                for c in col_range:
                    for row_sample in row_samples:
                        n_r = row_sample[0] + r
                        n_c = row_sample[1] + c
                        encoded_image.append(orig_image[n_r][n_c])
                        all_samples += [[n_r, n_c]]
    if len(encoded_image) != len(input_data):
        print("ERROR encoded image has different length")
    if encoded_image.count(0) != input_data.count(0):
        print("ERROR encoded image has different number of 0")
    if encoded_image.count(1) != input_data.count(1):
        print("ERROR encoded image has different number of 1")
    else:
        print("encoded image has {} of 1s".format(encoded_image.count(1)))
        print("encoded image has {} of 0s".format(encoded_image.count(0)))
        print("input data has {} of 1s".format(input_data.count(1)))
        print("input data has {} of 0s".format(input_data.count(0)))
    if encoded_image != input_data:
        print("ERROR encoded image is different from provided input")
        print("encoded image {}".format(encoded_image))
        print("input data {}".format(input_data))
    else:
        print("encoded image == input data!!")


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
    # adam7_encode(input_3[1], image_3_orig)
    adam7_decode(input_3)
