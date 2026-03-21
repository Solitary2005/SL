# 这个题没做出来的原因是认为这些操作是不可交换顺序的
# 但实际上，由于乘的系数都是k所以可以交换顺序
# 旋转可以看作角度和，然后一次性转这个角度，所以也可以交换顺序

''' 
######################### version 1
import sys
import math
input = sys.stdin.readline

n, m = map(int, input().split())
options = []
for s in range(n):
    op, info = input().split()
    options.append((int(op), float(info)))
    

for q in range(m):
    i, j, x, y = map(int, input().split())
    res = [x, y]

    for idx in range(i-1, j):
        op, info = options[idx]
        if op == 1:
            res[0] *= info
            res[1] *= info
        elif op == 2:
            old_x = res[0]
            old_y = res[1]
            res[0] = old_x*math.cos(info) - old_y*math.sin(info)
            # import ipdb;ipdb.set_trace()
            res[1] = old_x*math.sin(info) + old_y*math.cos(info)
    res[0] = str(res[0])
    res[1] = str(res[1])
    print(" ".join(res))
'''

######################### version 2
import sys
import math
input = sys.stdin.readline

n, m = map(int, input().split())
options = [(1, 0)]
angle_now = 0
queeze = 1
for s in range(n):
    op, info = input().split()
    if int(op) == 1:
        queeze *= float(info)
    elif int(op) == 2:
        angle_now += float(info)
    options.append((queeze, angle_now))

for idx in range(m):
    i, j, x, y = map(int, input().split())
    res_x = x
    res_y = y
    queeze_cur = options[j][0] / options[i-1][0]
    res_x *= queeze_cur
    res_y *= queeze_cur
    angle_cur = options[j][1] - options[i-1][1]
    old_x = res_x
    old_y = res_y
    res_x = old_x * math.cos(angle_cur) - old_y * math.sin(angle_cur)
    res_y = old_x * math.sin(angle_cur) + old_y * math.cos(angle_cur)
    res_l = [str(res_x), str(res_y)]
    print(" ".join(res_l))


