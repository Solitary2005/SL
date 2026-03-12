# import sys
# import numpy as np
# n, m, k = sys.stdin.readline().split()
# n, m, k = int(n), int(m), int(k)

# # t in [q+k,q+k+c)
# t = np.zeros((n,))
# c = np.zeros((n,))
# for i in range(n):
#     t_i, c_i = sys.stdin.readline().split()
#     t_i, c_i = int(t_i), int(c_i)
#     t[i] = t_i
#     c[i] = c_i

# for i in range(m):
#     q = int(input())
#     tmp_min = np.array([q+k]).repeat(n) #(n,)
#     tmp_max = np.array([q+k]).repeat(n) + c #(n,)
#     tmp = (t - tmp_min) * (tmp_max - t)
#     res = len(np.where(tmp >= 0)[0])
# print(res)

# 区间覆盖问题 -- 标准解法：差分数组+前缀和
'''
问题特征：有n个区间，m个查询，求对于每个查询，有多少个区间覆盖了该查询

前缀和通常用来快速求一个数组的某个区间和：
对于数组a，希望求a[l]到a[r]的和，可以先对a进行前缀和求解，即pre[i] = pre[0]+...+pre[i], 则a[l]到a[r]的和为pre[r]-pre[l-1]

差分数组可用于快速给一个数组的某个区间统一加上一个值：
即 有一个区间，我们想给区间 [L, R] 每个位置加一个常数scaler
'''
import sys
max_off = 2*10**5
diff = [0] * (max_off+1)
input = sys.stdin.readline
n, m, k = map(int, input().split())
info = []
for _ in range(n):
    t_i, c_i = map(int, input().split())
    L = t_i - k - c_i + 1
    R = t_i - k
    if R < 1:
        continue
    left = max(L, 1)
    right = R
    diff[left] += 1
    diff[right+1] -= 1

prefix = [0] * (max_off+1)
for i in range(1, max_off+1):
    prefix[i] = prefix[i-1] + diff[i]

for i in range(m):
    q = int(input())
    print(prefix[q])

    


    
