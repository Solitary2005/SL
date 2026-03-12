import sys
n, m, L = sys.stdin.readline().split()
n, m, L = int(n), int(m), int(L)
h = [0] * L
for i in range(n):
    a = sys.stdin.readline().split()
    # import ipdb; ipdb.set_trace()
    for j in range(m):
        h[int(a[j])] += 1
# import ipdb; ipdb.set_trace()
print(' '.join(map(str, h)))
#python list to str
#1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1