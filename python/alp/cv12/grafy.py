'''
soubour od cviciciho (vyresene prelevani.py)
'''
import sys

maxVolumes = [5, 3, 5]


class State:
    def __init__(self, v):
        self.v = v #
        self.act = ""
        self.prev = None

    def __repr__(self):
        return str(self.v) + self.act

    def expand(self):
        newStates = []
        # Ni nalit
        if self.v not in edges:
            return []
        for node in edges(self.v)):
            s = State(node)
            newStates.append(s)

        # # Vi vylit
        # for i in range(len(self.v)):
        #     if self.v[i] > 0:
        #         tmp = State(self.v)
        #         tmp.v[i] = 0
        #         tmp.act = "V{}".format(i)
        #         newStates.append(tmp)
        #
        # # iPj prelit z i do j
        # for i in range(len(self.v)):
        #     for j in range(len(self.v)):
        #         if i != j and self.v[i] > 0 and self.v[j] != maxVolumes[j]:
        #             tmp = State(self.v)
        #             rest = maxVolumes[j] - self.v[j]
        #             if self.v[i] > rest:
        #                 tmp.v[i] -= rest
        #                 tmp.v[j] += rest
        #             else:
        #                 tmp.v[j] += self.v[i]
        #                 tmp.v[i] = 0
        #             tmp.act = "{}P{}".format(i, j)
        #             newStates.append(tmp)
        # return newStates

f = open(sys.argv[1], "r")
edges = {}
for line in f:
    node1, node2, = list(map(int, line.strip().split()))
    if node1 not in edges:
        edges[node1] = []

    edges[node1].append(node2)
f.close()
print("edges", edges)

start = State(5)

goal = 1

openList = []
openList.append(start)
isInOpen = {}

while openList:
    actual = openList.pop(0)
    print(actual)
    if actual.v == goal:
        print("Huarra")
        while actual != None:
            print(actual)
            actual = actual.prev

        break

    states = actual.expand()

    for state in states:
        if not str(state.v) in isInOpen:
            state.prev = actual
            openList.append(state)
            isInOpen[str(state.v)] = 1