import sys

DEBUG_PRINTS = True


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
    ret_val = circle[direction:] + circle[:direction]
    return ret_val


ROTATION_P = 1
ROTATION_M = -1

if __name__ == '__main__':
    # red_balls = list(map(int, input().split()))
    # green_balls = list(map(int, input().split()))
    filename = sys.argv[1]
    red_circle, green_circle = read_balls(filename)
    debug_print("red balls={}, green balls={}".format(red_circle, green_circle), DEBUG_PRINTS)
    rp = rotate_circle(red_circle, ROTATION_P)
    rm = rotate_circle(red_circle, ROTATION_M)
    debug_print("rp={}, rm={}".format(rp, rm), DEBUG_PRINTS)
