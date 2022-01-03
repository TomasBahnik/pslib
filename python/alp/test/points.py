# hodnoty : 0.0 1.0 2.0 3.0
# import sys
#
#
# def load_values(vstup):
#     vstup = list(map(float, input().strip().split()))  # chybelo strip
#     bod_1 = vstup[0:2]
#     bod_2 = vstup[2:5]
#     if len(vstup) / 2 != int:
#         sys.exit(1)
#     else:
#         return bod_1, bod_2
#
#
# for a in load_values(sys.argv[1]):
#     print(a)
#
'''
reseni
'''
nums = list(map(float, input().strip().split()))
pts = []
for i in range(len(nums) // 2):
    x = nums[2 * i + 0]
    y = nums[2 * i + 1]

cx = 0
cy = 0
for p in pts:
    cx += p[0]
    cy += p[1]
cx /= len(pts)
cy /= len(pts)

minInd = None
minDist = None
for i in range(len(pts)):
    dx = pts[i][0] - cx
    dy = pts[i][1] - cy
    d = dx * dx + dy * dy
    if minInd == None or d < minDist:
        minDist = d
        minInd = i

for i in range(len(pts)):
    dx = pts[i][0] - 0
    dy = pts[i][1] - 0
    r = dx * dx + dy * dy
    cnt = 0
    for j in range(len(pts)):
        dx = pts[j][0] - 0
        dy = pts[j][1] - 0
        r2 = dx * dx + dy * dy
        if r2 <= r: # dulezite mensi nebo rovno !!
            cnt += 1
    if cnt == len(pts) // 2:
        print(minInd, i)