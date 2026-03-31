# import sys
# data = sys.stdin.buffer.read().split()
# it = iter(data)
# n = int(next(it))
# m = int(next(it))
# K = [int(next(it)) for _ in range(m)] # 变换前
# A = [int(next(it)) for _ in range(n)] # 变换后


#  & 用于取位，>> 用于移动位，<< 用于放置位，| 用于组合位
import sys
input_data = sys.stdin.read().split()
n = int(input_data[0])
m = int(input_data[1])
Ki = list(map(int, input_data[2:m+2]))
Ai = list(map(int, input_data[m+2:]))
def f(x,k):
    return ((x*x+k*k)&7)^k
def g(x,k):
    c = x&7
    b = (x>>3)&7
    a = (x>>6)&7
    return (b<<6)|((c^f(b,k))<<3)|(a^f(c,k))
std_res = [0]*512   # 单射关系(输出就512种)，构造输出->输入映射表
for f0 in range(512): # 0-512正向求解
    t = f0
    for k in Ki:
        t = g(t,k)
    std_res[t]=f0   # 记录输出输入对
print(*[std_res[ai] for ai in Ai],sep=' ')  # 遍历Ai查表输出

