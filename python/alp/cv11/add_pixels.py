import copy
def add_pixels(image):
    image_add = []
    col_value = -1
    row_value = -1
    image_add = copy.deepcopy(image)
    for row in image:
        row_value += 1
        for col in row:
            col_value += 1
            if col_value == img_width - 1: #sirka pole
                col_value = -1
            if col == 1:
                image_add[row_value][col_value + 1] = 1
                image_add[row_value + 1][col_value] = 1
                image_add[row_value + 1][col_value + 1] = 1
    # print("Adding pixels")
    return image_add