import sys
input = sys.stdin.readline

b, c, l, r = map(int, input().split())
if l % 2 == 0:
    start = l
else:
    start = l + 1

if r % 2 == 0:
    end = r
else:
    end = r - 1 

def fuc(x):
    return x**2 + b*x + c

res = 0
for i in range(start, end+1, 2):
    res += fuc(i)

print(res*2)