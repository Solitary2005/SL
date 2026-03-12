import sys
input = sys.stdin.readline
n, L, s = map(int, input().split())
ans = 0
# 只会在L-s
tree = []
for i in range(n):
    x, y = map(int, input().split())
    tree.append((x, y))

pic = []
for j in range(s+1):
    row = [int(x) for x in input().split()]
    pic.append(row)
    # for i in range(len(row)):
    #     if int(row[i]) == 1:
    #         pic.append((s - j, i))
pic.reverse()

for dx, dy in tree:
    if dx + s > L or dy + s > L:
        continue
    cur_map = [[0]*(s+1) for _ in range(s+1)]
    for x, y in tree:
        x -= dx
        y -= dy
        if 0 <= x <= s and 0 <= y <= s:
            cur_map[x][y] = 1

    ans += cur_map == pic


print(ans)     


