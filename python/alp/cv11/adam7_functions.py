import sys

from alp.cv11.adam7_alg import column, samples_positions, empty_image


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
    encoded_image = []
    for p in range(1, 8):
        samples = samples_positions[p]
        for r in row_range:
            for row_samples in samples:
                for c in col_range:
                    for row_sample in row_samples:
                        n_r = row_sample[0] + r
                        n_c = row_sample[1] + c
                        encoded_image.append(orig_image[n_r][n_c])
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
        samples = samples_positions[p]
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