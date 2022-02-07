import sys


def count_char_in_word(word, char):
    shift = -1
    count = 0
    while True:
        try:
            shift = word.index(char, shift + 1)
            count += 1
        except ValueError as ve:
            print(ve)
            break
    return count


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


def test():
    test_output("ahghiiimasftrgssktejj", 'j')
    test_output("ahghiiimasftirgsisktejj", 'i')


if __name__ == '__main__':
    # is_empty(sys.argv[1])
    # words_contains_letters(sys.argv[1])
    print(len(words_contains_letters(sys.argv[1])))
    # test()
    sys.exit(0)
