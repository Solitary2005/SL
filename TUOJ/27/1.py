import sys
input = sys.stdin.readline

n, m = map(int, input().split())

a = input().split()
b = ""
c = []
c.append(1)
tmp = 1
all_two = True
for i in range(n):
    if int(a[i]) != 2:
        all_two = False
    tmp *= int(a[i])
    c.append(tmp)
    if i == 0:
        b1 = m % tmp
        b_tmp = b1
        b = str(b1)
    else:
        b_i = ((m % tmp) - b_tmp) / c[i]
        b += ' '+str(int(b_i))
        b_tmp = b_tmp + c[i] * b_i

print(b)

# m=b1+2b2+4b3+...+2^(n-1)bn

        