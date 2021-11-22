# t = 'A = "ASDADSADA"  #COMMENT'
# print(t[:t.index('#')])


def skip(text):
    state = 0
    for letter in text:
        if state == 0:
            if letter == '#':
                state = 1
            elif letter == '"':
                state = 2
                print(letter, end="")
            else:
                print(letter, end="")
        elif state == 2:
            print(letter, end="")
            if letter == '"':
                state = 0
        elif state == 1:
            pass


skip('abc"ABC#123"#comment')
