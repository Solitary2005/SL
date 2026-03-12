import sys
input = sys.stdin.readline

n, x = map(int, input().split())
'''
01背包问题
有一个背包，容量为N，有m个物品，每个物品具有重量v_i，价值w_i，每个物品最多只能选一次；
求如何选择物品装入背包，使得背包内物品的总价值最大，且总重量不超过背包容量
'''
sum = 0
a = []
for i in range(n):
    a_i = int(input())
    a.append(a_i)
    sum += a_i


dp = [[0] * (sum - x + 1) for _ in range(n+1)]
# dp[i][j]
# 考虑前 i 个物品（从第1个到第i个），在背包容量为 j 的情况下，能获得的最大价值
for i in range(1, n+1):
    for j in range(sum - x + 1):
        if j < a[i-1]:
            dp[i][j] = dp[i-1][j]
        else:
            dp[i][j] = max(dp[i-1][j], dp[i-1][j-a[i-1]] + a[i-1])

print(sum - dp[n][sum - x])