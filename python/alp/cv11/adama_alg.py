total_passes = 7
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


def test(i):
    tot = 0
    img_w = i[0][0]
    img_h = i[0][1]
    img_size = img_w * img_h
    for p in range(1, 8):
        s = img_pass(i, p)
        tot += s
        debug_print("total samples_in_pass {}: {}, fraction {}".format(p, tot, img_size // tot), DEBUG_PRINTS)


if __name__ == "__main__":
    test(input_1)
    print("\n")
    test(input_2)
