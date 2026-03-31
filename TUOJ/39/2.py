import sys
input = sys.stdin.readline

n, L = map(int, input().split())
A = []

template = [[1]*9 for _ in range(5)]
for (i, j) in [(1,1),(1,2),(1,4),(1,5),(1,7),(2,1),(2,2),(2,8),
               (3,1),(3,2),(3,3),(3,4),(3,7),(3,8),(4,7),(4,8)]:
    template[i][j] = 0

for i in range(n):
    row = list(map(int, input().split()))
    A.append(row)

# import ipdb;ipdb.set_trace()

# for k in range(1, L):
#     for curx in range(n-4):
#         for cury in range(n-8):
#             if curx+5 > n or cury+9 > n:
#                 break
#             sucess = True
#             # curmap = A[curx:curx+5][cury:cury+9]
#             curmap = [row[cury:cury+9] for row in A[curx:curx+5]]
#             curmap_ = deepcopy(curmap)
#             # import ipdb;ipdb.set_trace()
#             # assert len(curmap) == 5
#             for x in range(5):
#                 for y in range(9):
#                     curmap_[x][y] = int(curmap[x][y] >= k)
#                     # import ipdb;ipdb.set_trace()
#                     if curmap_[x][y] != template[x][y]:
#                         sucess = False
#                         break
#                 if sucess == False:
#                     break
#             if sucess == True:
#                 print(k)
#     # import ipdb;ipdb.set_trace()


# 如果k可行，则其一定大于A在template为0处的像素值，小于等于A在template为1处的像素值
# 初始化标记数组，长度为 L，下标对应 k
ok = [False] * L

# 遍历所有可能的子矩阵左上角
for curx in range(n-4):
    for cury in range(n-8):
        if curx+5 > n or cury+9 > n:
            break
        max_zero = -1
        min_one = L
        # 遍历 5x9 区域
        for x in range(5):
            for y in range(9):
                val = A[curx+x][cury+y]
                if template[x][y] == 0:   # 黑色位置
                    if val > max_zero:
                        max_zero = val
                else:                     # 白色位置
                    if val < min_one:
                        min_one = val
        # 区间 [max_zero+1, min_one] 内的 k 可行
        lo = max_zero + 1
        hi = min_one
        if lo <= hi:
            for k in range(lo, hi+1):
                ok[k] = True

# 输出所有可行的 k
for k in range(L):
    if ok[k]:
        print(k)
