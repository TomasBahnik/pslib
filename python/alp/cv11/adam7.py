adam7_pattern = [[1, 6, 4, 6, 2, 6, 4, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7],
                 [5, 6, 5, 6, 5, 6, 5, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7],
                 [3, 6, 4, 6, 3, 6, 4, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7],
                 [5, 6, 5, 6, 5, 6, 5, 6],
                 [7, 7, 7, 7, 7, 7, 7, 7]]

UNDEFINED_PIXEL = -1


def empty_image(w, h):
    b = []
    for i in range(h):
        b.append([UNDEFINED_PIXEL] * w)
    return b


def sample_positions(p):
    all_rows = []
    for i in range(len(adam7_pattern)):
        one_row = []
        for j in range(len(adam7_pattern[i])):
            if adam7_pattern[i][j] == p:
                one_row += [[i, j]]
        all_rows.append(one_row)
    return all_rows


# prepare samples positions once
samples_positions = {}
for p in range(1, 8):
    samples_positions[p] = sample_positions(p)


def column(matrix, i):
    return [row[i] for row in matrix]


def all_image_samples(col_range, row_range):
    all_samples = []
    for p in range(1, 8):
        for r in row_range:
            for row_samples in samples_positions[p]:
                for c in col_range:
                    for row_sample in row_samples:
                        n_r = row_sample[0] + r
                        n_c = row_sample[1] + c
                        all_samples += [[n_r, n_c]]
    return all_samples


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


def add_pixels_row(r):
    for i in range(len(r)):
        pixel = r[i]
        if pixel == UNDEFINED_PIXEL:
            r[i] = r[i - 1]  # TODO i > 0 ??


def add_pixels(image):
    h = len(column(image, 0))
    for r in range(h):
        if 0 in image[r] or 1 in image[r]:
            add_pixels_row(image[r])
        else:
            if r > 0:  # must not be first row
                image[r] = image[r - 1][:]
    return image


def print_image(decoded_image, add_pix):
    img = add_pixels(decoded_image) if add_pix else decoded_image
    for r in img:
        s = ''
        for pixel in r:
            s += str(pixel)
        s1 = s.replace('1', '*').replace('0', ' ')
        print(s1)


def adam7_test(test_inputs):
    for i in test_inputs:
        w = i[0][0]
        h = i[0][1]
        i_d = i[1]
        f = w * h // len(i_d)
        print("{}/{} {}x{}".format(1, f, w, h))
        image = adam7_decode(i)
        print_image(image, f > 1)


if __name__ == "__main__":
    img_width, img_height = list(map(int, input().split()))
    img_encoded = list(map(int, input().split()))
    img_input = [[img_width, img_height], img_encoded]
    img_size = img_width * img_height
    img_decoded = adam7_decode(img_input)
    add = img_size > len(img_encoded)
    print_image(img_decoded, add)
    # adam7_test(test_inputs_24_24)
    # adam7_test(test_inputs_24_24)
