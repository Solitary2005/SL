import sys
input = sys.stdin.readline

n, m = map(int, input().split())

reward = list(map(int, input().split()))
reward.insert(0, 0)


# def get_max_reward(day):
#     global apples
#     global res
#     if apples == 0:
#         return 0
#     if day == 0:
#         return 0
#     base_reward = get_max_reward(day-1)
#     best_apple = 0
#     best_reward = 0
#     for a in range(1, min(apples,m)+1):
#         reward_now = base_reward + reward[a]
#         if reward_now > best_reward:
#             best_reward = reward_now
#             best_apple = a
    
#     res[day] = best_reward
#     apples -= best_apple
#     return best_reward

# 模板题：根据苹果数量动态规划
dp = [0] * (n+1)
for i in range(1, n+1):
    for j in range(1, min(i, m)+1):
        dp[i] = max(dp[i], dp[i-j] + reward[j]) 

print(dp[n])

'''
动态规划思路模板
动态规划的核心是将原问题拆分成多个重叠的子问题，并用一个状态表示子问题的答案
1. 定义状态
常见状态定义：
    一维：dp[i] 表示处理前 i 个元素的最优值（如苹果问题：dp[i] 表示喂完 i 个苹果的最大收益）。
    二维：有时需要额外维度，如背包问题中需要记录剩余容量。
    注意状态要足够“无后效性”：未来决策只取决于当前状态，与如何达到该状态无关
2. 推导状态转移方程
    思考：当前状态 dp[i] 与更小规模的状态有什么关系？
    通常需要枚举所有可能的“最后一步”操作，取最优。
3. 确定初始化状态和边界条件
    最小的子问题通常可以直接给出答案，比如 dp[0] = 0（没有苹果，收益为 0）。
    注意状态是否可达，不可达的状态可以初始化为负无穷（如果求最大值）或正无穷（如果求最小值），避免被错误更新。
4. 确保循环遍历时，依赖的状态已经被计算过
    若 dp[i] 只依赖更小的 i，则从小到大遍历 i。
    若依赖更大或更小的，可能需要特殊顺序（如二维背包）

经典模板题
线性 DP（如最长上升子序列、最大子段和）
背包问题（0/1背包、完全背包、多重背包）
区间 DP（合并石子等）
树形 DP（树上依赖）
状态压缩 DP（集合类问题）
'''