maxVolumes = [5, 3, 5]


class State:
    def __init__(self, v):
        self.v = v[:]
        self.act = ""
        self.prev = None

    def __repr__(self):
        return str(self.v) + str(self.act)

    def expand(self):
        newStates = []
        # akce Ni - nalit
        for i in range(len(self.v)):
            if self.v[i] < maxVolumes[i]:
                tmp = State(self.v)
                tmp.v[i] = maxVolumes[i]
                tmp.act = "N{}".format(i)
                newStates.append(tmp)

        # akce Vi - vylit
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                if self.v[i] > 0 and self.v[j] < maxVolumes[j]:
                    tmp = State(self.v)
                    tmp.v[i] = 0
                    tmp.act = "V{}".format(i)
                    newStates.append(tmp)

        # prelit z i do j
        # nejtezzsi krok, zkusit doma !!
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                tmp = State(self.v)
                tmp.act = "{}P{}".format(i, j)
                rest = maxVolumes[j] - self.v[j]
                if self.v[i] > rest:
                    tmp.v[j] += rest
                    tmp.v[i] -= rest
                else:
                    tmp.v[j] += tmp.v[i]
                    tmp.v[i] = 0
                newStates.append(tmp)

        return newStates


start = State([5, 0, 0])
states = start.expand()
print(states)

goal = [3, 2, 0]
"cvika12"
openList = []
openList.append(start)  # pole referenci
known = {}
while len(openList) > 0:
    s = openList.pop(0)
    if s.v == goal:
        while s != None:
            print(s)
            s = s.prev
        print("Huraa")
        break

    exp = s.expand()  # pole referenci
    for state in exp:
        if not str(state.v) is known:
            state.prev = s
            openList.append(state)
            known[str(state.v)] = 1
