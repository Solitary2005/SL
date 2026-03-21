# import sys
# input = sys.stdin.readline

# n, m = map(int, input().split())
# codes = []
# for _ in range(n):
#     code = list(map(int, input().split()))
#     codes.append(code)

# res = [0] * n
# for i in range(n):
#     min_idx = None
#     for j in range(n):
#         if i == j:
#             continue
#         # 检查是否每一维都大于
#         ok = True
#         for k in range(m):
#             if codes[j][k] <= codes[i][k]:
#                 ok = False
#                 break
#         if ok:
#             if min_idx is None or j < min_idx:
#                 min_idx = j
#     if min_idx is not None:
#         res[i] = min_idx + 1  # 输出编号
#     else:
#         res[i] = 0

# for t in res:
#     print(t)