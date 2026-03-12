import sys
n, N = sys.stdin.readline().split()
A = sys.stdin.readline().split()
A.insert(0, '0')
res = 0
# import ipdb;ipdb.set_trace()
# print(len(A))
for i in range(len(A)-1):
    # if i == len(A)-1:
    #     break
    # print(i)
    res += i*(int(A[i+1])-int(A[i]))
res += int(n)*(int(N)-int(A[-1]))
print(res)