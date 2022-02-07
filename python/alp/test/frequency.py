import sys


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


if __name__ == '__main__':
    is_empty(sys.argv[1])
    words_contains_letters(sys.argv[1])
