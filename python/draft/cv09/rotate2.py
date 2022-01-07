DEBUG_PRINTS = True

GREEN_BALL = 1
GREEN_CIRCLE = 1
RED_BALL = 0
RED_CIRCLE = 0
CIRCLE_MOVE_P = 1
CIRCLE_MOVE_M = -1


def debug_print(message, print_debug):
    if print_debug:
        print(message)


def read_balls(input_file):
    balls = []
    f = open(input_file, "r")
    r_circle = list(map(int, f.readline().strip().split()))  # precti 1. radek ze souboru
    g_circle = list(map(int, f.readline().strip().split()))
    # for line in f:
    #     numbers = list(map(int, line.strip().split()))  # precti vsechna cisla na dalsich radcich
    #     color = numbers[0]  # prvni z nich je barva kamene
    #     coords = numbers[1:]  # zbyle jsou souradnice r1 c1 ... rn cn
    #     cells = []  # prevedeme [r1,c1 ... rn,cn] na pole cells = [[r1,c1], ... [rn,cn]]
    #     for i in range(len(coords) // 2):
    #         cells.append([coords[2 * i + 0], coords[2 * i + 1]])
    #     stones.append([color, cells])
    # f.close()
    return r_circle, g_circle


def rotate_circle(circle, direction):
    d = - direction
    ret_val = circle[d:] + circle[:d]
    return ret_val


def play(game, moves):
    for move in moves:
        c1, d = move
        new_c = rotate_circle(game[c1], d)
        game[c1] = new_c
        c2 = GREEN_CIRCLE if c1 == RED_CIRCLE else RED_CIRCLE
        # 0 and 2 must be the same
        game[c2][0] = game[c1][0]
        game[c2][2] = game[c1][2]


def print_game(game):
    debug_print("r={}".format(game[RED_CIRCLE]), DEBUG_PRINTS)
    debug_print("g={}\n".format(game[GREEN_CIRCLE]), DEBUG_PRINTS)


# a=[0, 1, 2, 3, 4, 5]
# m=[1, 2, 3, 4, 5, 0],True
# a=[0, 1, 2, 3, 4, 5]
# p=[5, 0, 1, 2, 3, 4],True
def test_moves():
    a = [0, 1, 2, 3, 4, 5]
    m_expected = [1, 2, 3, 4, 5, 0]  # index increased by -1 (m)
    p_expected = [5, 0, 1, 2, 3, 4]  # index increased by +1 (p)
    m = rotate_circle(a, CIRCLE_MOVE_M)
    p = rotate_circle(a, CIRCLE_MOVE_P)
    debug_print("a={}".format(a), DEBUG_PRINTS)
    debug_print("m={},{}".format(m, m == m_expected), DEBUG_PRINTS)
    debug_print("a={}".format(a), DEBUG_PRINTS)
    debug_print("p={},{}\n".format(p, p == p_expected), DEBUG_PRINTS)


def test_inputs(file, moves):
    debug_print('{}'.format(file), DEBUG_PRINTS)
    red_circle, green_circle = read_balls(file)
    # positions R=0, G=1
    game = [red_circle, green_circle]
    print_game(game)
    play(game, moves)
    print_game(game)


if __name__ == '__main__':
    # test_moves()
    # red_balls = list(map(int, input().split()))
    # green_balls = list(map(int, input().split()))

    # input_1.txt : (1,p)
    moves = [(GREEN_CIRCLE, CIRCLE_MOVE_P)]
    test_inputs('input_1.txt', moves)

    # input_2.txt : (1,p)(0,m)
    moves = [(GREEN_CIRCLE, CIRCLE_MOVE_P), (RED_CIRCLE, CIRCLE_MOVE_M)]
    test_inputs('input_2.txt', moves)

    # input_3.txt : (0,m)(1,p)(1,p)(0,p)(1,p)(0,p)
    moves = [(RED_CIRCLE, CIRCLE_MOVE_M), (GREEN_CIRCLE, CIRCLE_MOVE_P), (GREEN_CIRCLE, CIRCLE_MOVE_P),
             (RED_CIRCLE, CIRCLE_MOVE_P), (GREEN_CIRCLE, CIRCLE_MOVE_P), (RED_CIRCLE, CIRCLE_MOVE_P)]
    test_inputs('input_3.txt', moves)
