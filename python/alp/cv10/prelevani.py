maxVolumes = [5, 4, 1]


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
            tmp = State(self.v)
            tmp.v[i] = maxVolumes[i]
            tmp.act = "N{}".format(i)
            newStates.append(tmp)

        # akce Vi - vylit
        for i in range(len(self.v)):
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


start = State([0, 0, 0])
states = start.expand()
print(states)
