import sys
input = sys.stdin.readline

q = int(input())

# 质因数分解快速方法：试除法
# 从2开始试除，如果j是n的因子，就把j除干净; 
# 只用枚举到根号n，因为大于根号n的因子的指数一定是1（p>根号n, 则p^2>n, 所以必然只能为1）

for i in range(q):
    n, k = map(int, input().split())
    res = 1
    j = 2
    while (j * j <= n):
        if n % j == 0:
            c = 0
            while (n % j == 0):
                n = n // j
                c += 1
            if c >= k:
                res *= (j**c)
        j += 1
    print(res)
