"""
INPUTS
0. 1. -1. 0.5
1. 0. -1. -1.5

---> 1 (idx min abs f(x,y))
     2 (idx druhe max hodnoty)
     2 (pocet kladnych hodnot)


1.
2.

---> 0
     NONE
     0

1.0 2.5
2.0

---> ERROR
"""
def load_input(inp):
    nums = list(map(float, inp.strip().split()))
    print(nums)

if __name__ == '__main__':
    load_input(input())