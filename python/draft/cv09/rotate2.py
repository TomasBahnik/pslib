import copy

DEBUG_PRINTS = True

GREEN_CIRCLE = 1
RED_CIRCLE = 0
CIRCLE_MOVE_P = 1
CIRCLE_MOVE_M = -1
CIRCLE_SYMBOLS = {CIRCLE_MOVE_P: 'p', CIRCLE_MOVE_M: 'm'}


def read_circles(input_file):
    f = open(input_file, "r")
    r_circle = list(map(int, f.readline().strip().split()))  # precti 1. radek ze souboru
    g_circle = list(map(int, f.readline().strip().split()))
    return [r_circle, g_circle]


def rotate_circle(circle, direction):
    d = - direction
    ret_val = circle[d:] + circle[:d]
    return ret_val


def play(game, move):
    c1, d = move
    new_game = copy.deepcopy(game)
    new_c = rotate_circle(new_game[c1], d)
    new_game[c1] = new_c
    c2 = GREEN_CIRCLE if c1 == RED_CIRCLE else RED_CIRCLE
    # 0 and 2 must be the same
    new_game[c2][0] = new_c[0]
    new_game[c2][2] = new_c[2]
    return new_game


class State:
    def __init__(self, i_circles):
        self.circles = copy.deepcopy(i_circles)
        self.act = ""
        self.prev = None

    def __repr__(self):
        return str(self.act)
        # return str(self.circles) + str(self.act)

    def expand(self):
        newStates = []
        # akce rotate p
        for i in range(len(self.circles)):
            tmp = State(self.circles)
            tmp.circles = play(self.circles, [i, CIRCLE_MOVE_P])
            tmp.act = "({},{})".format(i, CIRCLE_SYMBOLS[CIRCLE_MOVE_P])
            newStates.append(tmp)

        # akce rotate m
        for i in range(len(self.circles)):
            tmp = State(self.circles)
            tmp.circles = play(self.circles, [i, CIRCLE_MOVE_M])
            tmp.act = "({},{})".format(i, CIRCLE_SYMBOLS[CIRCLE_MOVE_M])
            newStates.append(tmp)

        return newStates


if __name__ == '__main__':
    # test_moves()
    # red_balls = list(map(int, input().split()))
    # green_balls = list(map(int, input().split()))
    initial_circles = read_circles('input_3.txt')
    goal = [[1, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 1]]
    # goal = initial_circles
    start_state = State(initial_circles)
    states = start_state.expand()
    # print(states)

    open_states = [start_state]
    known = {}
    while len(open_states) > 0:
        s = open_states.pop(0)
        if s.circles == goal:
            while s != None:
                print(s, end=',')
                s = s.prev
            # print("Huraa")
            break

        exp = s.expand()  # pole referenci
        for state in exp:
            if not str(state.circles) is known:
                state.prev = s
                open_states.append(state)
                known[str(state.circles)] = 1
