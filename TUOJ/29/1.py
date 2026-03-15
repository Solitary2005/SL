import sys
input = sys.stdin.readline

n, a, b = map(int, input().split())
res = 0
for i in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    l_b_x = max(x1, 0)
    l_b_y = max(y1, 0)
    r_t_x = min(x2, a)
    r_t_y = min(y2, b)
    if l_b_x < r_t_x and l_b_y < r_t_y:
        res += (r_t_x - l_b_x) * (r_t_y - l_b_y)

print(res)