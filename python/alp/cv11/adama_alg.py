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

input_3 = [[16, 16], []]


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

    pos_1 = idx_of_passes[1][0]
    sam = samples[1]
    r, c = pos_1
    for f in [0, 7, 15]:
        for g in [0, 7, 15]:
            e_i[r + f][c + g] = sam.pop(0)
    print(e_i)


if __name__ == "__main__":
    test(input_1)
    print("\n")
    # test(input_2)
