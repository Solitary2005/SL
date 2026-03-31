import sys
from collections import deque
input = sys.stdin.readline

n, k = map(int, input().split())
x, y = map(int, input().split())

# 广度优先搜索，按层记录步数

directions = [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]
visited = [ [False]* (n+1) for _ in range(n+1) ]
# res_set = set()
# res_set.add((x, y))
q = deque()
q.append((x, y, 0))
visited[x][y] = True
num = 1

while q:
    curx, cury, step = q.popleft()
    if step >= k:
        continue
    for dx, dy in directions:
        newx, newy = curx+dx, cury+dy
        if 1 <= newx <= n and 1 <= newy <= n:
            # res_set.add((newx, newy))
            if not visited[newx][newy]:
                q.append((newx, newy, step+1))
                visited[newx][newy] = True
                num += 1
# import ipdb; ipdb.set_trace()
# print(step)
print(num)
            