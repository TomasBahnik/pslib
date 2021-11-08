result = []


def flatten(array):
    for item in array:
        if type(item) == list:
            flatten(item)
        else:
            result.append(item)


a = [1, 2, [3, [4, 5], 6, [7]], [8, 9], 10]
print(a)
flatten(a)
print(result)
