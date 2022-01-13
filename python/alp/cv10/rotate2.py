import copy

red = list(map(int, input().strip().split()))
green = list(map(int, input().strip().split()))
both = [red, green]

goal = [[1, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 1]]
"""
INPUTS:
1 0 1 0 0 0
1 1 1 0 1 1
"""
RED_CIRCLE = 0
GREEN_CIRCLE = 1
CIRCLE_MOVE_P = 1
CIRCLE_MOVE_M = -1
SYMBOL = {CIRCLE_MOVE_P: "p", CIRCLE_MOVE_M: "m"}


def rotate(cir, dir):
    rotateted = cir[-dir:] + cir[:-dir]
    return rotateted


def move(circles, parametres):
    """c = colour(primary red / c=0 ---> red / c=1 ---> green)"""
    c, d = parametres
    new_circles = copy.deepcopy(circles)
    rotate_new_circles = rotate(new_circles[c], d)
    new_circles[c] = rotate_new_circles
    c2 = GREEN_CIRCLE if c == RED_CIRCLE else RED_CIRCLE
    """points in both circles ---> 0 and 2"""
    new_circles[c2][0] = rotate_new_circles[0]
    new_circles[c2][2] = rotate_new_circles[2]
    return new_circles


class State:
    def __init__(self, both_2):
        self.both = copy.deepcopy(both_2)
        self.act = ""
        self.prev = None

    def __repr__(self):
        str(self.both) + str(self.act)
        return

    def expand(self):
        new_state = []

        """move P"""
        for i in range(len(self.both)):
            tmp = State(self.both)
            tmp.both = move(self.both, [i, CIRCLE_MOVE_P])
            tmp.act = "({},{})".format(i, SYMBOL[CIRCLE_MOVE_P])
            new_state.append(tmp)

        """move M"""
        for i in range(len(self.both)):
            tmp = State(self.both)
            tmp.both = move(self.both, [i, CIRCLE_MOVE_M])
            tmp.act = "({},{})".format(i, SYMBOL[CIRCLE_MOVE_M])
            new_state.append(tmp)
        return new_state


start = State(both)
state = start.expand()

openList = [start]
known = {}

while len(openList) > 0:
    s = openList.pop(0)
    if s.both == goal:
        while s != None:
            print(s)
            s = s.prev
        print("Huraa")
        break

    exp = s.expand()
    for state in exp:
        if not str(state.both) is known:
            state.prev = s
            openList.append(state)
            known[str(state.both)] = 1
