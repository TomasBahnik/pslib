import sys

total_count = 0


def count_char_in_word(word, char, shift):
    global total_count
    try:
        shift = word.index(char, shift)
        total_count += 1
        count_char_in_word(word, char, shift + 1)
    except ValueError as ve:
        # print(ve)
        print("znak {} not in {}".format(char, word))
    return total_count


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


if __name__ == '__main__':
    # is_empty(sys.argv[1])
    # words_contains_letters(sys.argv[1])
    print(len(words_contains_letters(sys.argv[1])))
    # print(count_char_in_word("abicdfgihni", "i", 0))
    sys.exit(0)
