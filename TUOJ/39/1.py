import sys
input = sys.stdin.readline

n, a = map(int, input().split())
m = 0

for i in range(n):
    x, y = input().split()
    x, y = float(x), float(y)
    d = x**2 + y**2
    if d <= a**2:
        m += 1

print(4.0*m/n)
