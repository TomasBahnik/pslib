import sys


def count_char_in_word(word, char):
    tmp = [z for z in word if z == char]
    return len(tmp)


def load_input(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(line.strip())
        # print(pole)
    return pole


def is_empty(file):
    if len(load_input(file)) == 0 and input() != 0:
        print(0)
        print("NEEXISTUJE")
        sys.exit(0)


def words_contains_letters(file, inp):
    p = load_input(file)
    pole = []
    for slovo in p:
        count = 0
        for z in inp:
            if z in slovo:
                count += 1
            if count == len(inp):
                count = 0
                # print(slovo)
                pole.append(slovo)
    return pole


# def test_output(slovo, znak):
#     print("'{}' in '{}' : {}x ".format(znak, slovo, count_char_in_word(slovo, znak)))
#
#
# def test():
#     test_output("ahghiiimasftrgssktejj", 'j')
#     test_output("ahghiiimasftirgsisktejj", 'i')


def max_contained_word(words, inp):
    if len(words) == 0:
        return "NEEXISTUJE"
    compare = []
    for w in words:
        counter = []
        for z in inp:
            counter.append(count_char_in_word(w, z))
        compare.append(sum(counter))
    max_value = max(compare)
    max_index = compare.index(max_value)
    # print(words[max_index])
    return words[max_index]


if __name__ == '__main__':
    # words_contains_letters(sys.argv[1])
    # test()
    inp_txt = sys.argv[1]
    inp = input()
    w_c_l = words_contains_letters(inp_txt, inp)
    print(len(w_c_l))
    print(max_contained_word(w_c_l, inp))
    sys.exit(0)
