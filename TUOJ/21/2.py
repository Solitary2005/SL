import sys

def predict(y, theta):
    if y < theta:
        return 0
    else:
        return 1

m = int(input())
y = [0] * m
r = [0] * m
res = {}
for i in range(m):
    y[i], r[i] = sys.stdin.readline().split()
    y[i] = int(y[i])
    r[i] = int(r[i])

# for i in range(m):
#     theta = y[i]
#     result = 0
#     for j in range(m):
#         if predict(y[j], theta) == r[j]:
#             result += 1
#     pre = res.get(result, -1)
#     if pre == -1:
#         res[result] = theta
#     elif theta > pre:
#         res[result] = theta
# # import ipdb; ipdb.set_trace()
# indice = max(res.keys())

# print(res[indice])
# for i in range(m):
#     theta = y[i]
#     result = np.array(y) < theta
#     result = result.astype(int)
#     result = np.sum(result == np.array(r))
#     pre = res.get(result, -1)
#     if pre == -1:
#         res[result] = theta
#     elif theta > pre:
#         res[result] = theta
# indice = np.argmax(list(res.keys()))
# print(res[indice])
    
# python返回最大/最小位置索引

items = sorted(zip(y, r))  # 按 y 升序
total_one = sum(r)

left_zero = 0
left_one = 0
best_acc = -1
best_theta = None

i = 0
n = m
while i < n:
    val = items[i][0]

    # 计算以 val 为阈值（严格 <）的准确数
    acc = left_zero + (total_one - left_one)
    if acc > best_acc or (acc == best_acc and (best_theta is None or val > best_theta)):
        best_acc = acc
        best_theta = val

    # 把所有 y == val 的样本移到左侧
    cnt_zero = 0
    cnt_one = 0
    while i < n and items[i][0] == val:
        if items[i][1] == 0:
            cnt_zero += 1
        else:
            cnt_one += 1
        i += 1
    left_zero += cnt_zero
    left_one += cnt_one

print(best_theta)