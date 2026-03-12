import sys
input = sys.stdin.readline

n = int(input())
a = input().split()
# import ipdb; ipdb.set_trace()
res_sum = 0
for i in range(n):
    res_sum += int(a[i])
res_mean = res_sum / n
tmp = 0
for i in range(n):
    tmp += (int(a[i]) - res_mean)**2
var = tmp / n
for i in range(n):
    f = (int(a[i])-res_mean) / (var)**(0.5)
    print(f)
    # if i != n-1:
    #     print('\n')