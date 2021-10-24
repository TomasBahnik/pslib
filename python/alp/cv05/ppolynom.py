def pp(poly):
    for i in range(len(poly)):
        if i > 0 and poly[i] == 0:
            continue
        if poly[i] >= 0:
            print("+",end="")
        if i == 0:
            print(poly[i],end=" ")
        elif i == 1:
            print(poly[i],end=" ")
        else:
            print(poly[i],"x^",i,end=" ", sep="")

a = [0,1,2,-3]
pp(a)