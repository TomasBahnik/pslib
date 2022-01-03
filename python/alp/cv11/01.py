openList = []
openList.append(start) # pole referenci
while len(openList)>0:
    s = openList.pop(0)
    exp = s.expand() #pole referenci
    for state in exp:
        openList.append(state)