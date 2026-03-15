import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())

info = []
max_t = -1
doc = []

def check(d):
    global res
    total = 0
    for i in range(n):
        t = info[i][0]
        c = info[i][1]
        if t > d:
            total += (t - d) * c
    if total <= m:
        res = d
        return 'left'
    return 'right'



for i in range(n):
    t_i, c_i = map(int, input().split())
    info.append((t_i, c_i))
    if t_i > max_t:
        max_t = t_i
res = max_t
l = k
r = max_t
while l < r:
    mid = (l + r) // 2
    if check(mid) == 'left':
        r = mid
    elif check(mid) == 'right':
        l = mid + 1
    
print(res)
        


# 暴力：
# res从k开始逐渐增大，计算所有土地都减到res天需要的资源总量，直到该量小于等于m

# 如何培养这种“二分感”
# 下次遇到类似问题时，可以问自己几个问题：

# 答案是不是一个整数，且范围已知？ ✅ 是

# 随着答案变大，可行性是不是单调变化？ （更大天数更容易可行）✅ 是

# 判断一个候选答案是否可行，是否容易计算？ ✅ 是（一次遍历）