from alp.cv11.adam7_data import quarter_24_8, input_1_16_24_24, input_1_8_24_24
from alp.cv11.adam7_data import full_24_8

adam7_pattern = [[1, 6, 4, 6, 2, 6, 4, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7],
                 [5, 6, 5, 6, 5, 6, 5, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7],
                 [3, 6, 4, 6, 3, 6, 4, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7],
                 [5, 6, 5, 6, 5, 6, 5, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7]]


def empty_image(w, h):
    b = []
    for i in range(h):
        b.append([0] * w)
    return b


def idx_of_pass(p):
    all_rows = []
    for i in range(len(adam7_pattern)):
        one_row = []
        for j in range(len(adam7_pattern[i])):
            if adam7_pattern[i][j] == p:
                one_row += [[i, j]]
        all_rows.append(one_row)
    return all_rows


idx_of_passes = {}
for p in range(1, 8):
    idx_of_passes[p] = idx_of_pass(p)


def column(matrix, i):
    return [row[i] for row in matrix]


def adam7_decode(test_input):
    img_w = test_input[0][0]
    img_h = test_input[0][1]
    decoded_image = empty_image(img_w, img_h)
    img_coded = test_input[1]
    w_r = img_w // 8
    r_r = img_h // 8
    row_range = [x * 8 for x in range(0, r_r)]
    col_range = [x * 8 for x in range(0, w_r)]
    all_samples = all_image_samples(col_range, row_range)
    for i in range(len(img_coded)):
        val = img_coded[i]
        coord = all_samples[i]
        decoded_image[coord[0]][coord[1]] = val
    return decoded_image


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


def print_image(decoded_image):
    for r in decoded_image:
        s1 = str(r).replace('1', '*').replace('0', ' ').replace(',', '').replace('[', '').replace(']', '')
        print(s1)


if __name__ == "__main__":
    # test_adam(24, 8)
    # adam7_encode(input_3[1], image_3_orig)
    print("1/4 24x8")
    image = adam7_decode(quarter_24_8)
    print_image(image)
    print("full 24x8")
    image = adam7_decode(full_24_8)
    print_image(image)
    print("1/16 24x24")
    image = adam7_decode(input_1_16_24_24)
    print_image(image)
    print("1/8 24x24")
    image = adam7_decode(input_1_8_24_24)
    print_image(image)
