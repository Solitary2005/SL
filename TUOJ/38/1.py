import sys
import math
input = sys.stdin.readline

def truncate_2f(x):
    return math.floor(x * 100) / 100

def truncate_1f(x):
    return math.floor(x * 10) / 10

k = int(input())
# for i in range(k):
#     mu, sigma, n = map(int, input().split())
#     m = (n - mu) / sigma
#     col = f"{truncate_2f(m):.2f}"
#     col = int(col[-1])
#     row = f"{truncate_1f(m):.1f}"
#     row = int(float(row)*10)
#     res = (str(row+1), str(col+1))
#     print(' '.join(res))

for _ in range(k):
    mu, sigma, n = map(int, input().split())
    m10 = (n - mu) * 10 // sigma
    m100 = (n - mu) * 100 // sigma
    row = m10 + 1          # 行号（从1开始）
    col = (m100 % 10) + 1  # 列号（从1开始）
    print(row, col)