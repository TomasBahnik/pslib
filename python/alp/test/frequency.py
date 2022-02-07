import sys


def count_char_in_word(word, char):
    shift = -1
    count = 0
    while True:
        try:
            shift = word.index(char, shift + 1)
            count += 1
        except ValueError as ve:
            break
    return count


def word_contains_letters(word, letters):
    total_count = 0
    for letter in letters:
        cnt = count_char_in_word(word, letter)
        if cnt == 0:
            return 0
        else:
            total_count += cnt
    return total_count


def words_letters(file, letters):
    words = load_input(file)
    w_l = []
    for word in words:
        w_l.append([word, word_contains_letters(word, letters)])
    return w_l


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


def words_contains_letters(file):
    p = load_input(file)
    inp = input()  # POLE!!
    pole = []
    for slovo in p:
        count = 0
        i = 0
        while i + 1 < len(inp):
            for i in range(0, len(inp)):
                if inp[i] in slovo:
                    count += 1
                if count == len(inp):
                    count = 0
                    print(slovo)
                    pole.append(slovo)
    return pole


def test_output(slovo, znak):
    print("'{}' in '{}' : {}x ".format(znak, slovo, count_char_in_word(slovo, znak)))


def test_1():
    test_output("ahghiiimasftrgssktejj", 'j')
    test_output("ahghiiimasftirgsisktejj", 'i')


def test(file, letters):
    x = words_letters(file, letters)
    c = [a[0] for a in x if a[1] > 0]
    m = [a[1] for a in x if a[1] > 0]
    max_cnt_idx = m.index(max(m))
    print(letters, "contained in :", c, "delka:", len(c))
    print(letters, "maximal count :", c[max_cnt_idx])


if __name__ == '__main__':
    # is_empty(sys.argv[1])
    # words_contains_letters(sys.argv[1])
    print(len(words_contains_letters(sys.argv[1])))
    # test(sys.argv[1], 'irg')
    sys.exit(0)
