import sys


def load_input(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(line.strip())
    return pole


def words_with_inp(inp):
    lenght = len(inp)
    words = [w for w in load_input(file) if w[-lenght:] == inp]
    return words


def shortest_word(words):
    words_len = []
    for i in range(len(words)):
        words_len.append(len(words[i]))
    sequence = words_len.index(min(words_len))
    return words[sequence]

if __name__ == '__main__':
    file = sys.argv[1]
    inp = input()
    # load_input(file)
    w_w_i = words_with_inp(inp)
    print(len(w_w_i))
    print(shortest_word(w_w_i))




