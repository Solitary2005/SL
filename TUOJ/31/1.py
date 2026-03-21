import sys
input = sys.stdin.readline

n, m = map(int, input().split())
deltax = 0
deltay = 0
for i in range(n):
    dx, dy = input().split()
    deltax += int(dx)
    deltay += int(dy)

for i in range(m):
    xi, yi = input().split()
    pstr = ""
    pstr += str(int(xi)+deltax)
    pstr += " "
    pstr += str(int(yi)+deltay)
    print(pstr)
    