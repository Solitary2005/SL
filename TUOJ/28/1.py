import sys 
input = sys.stdin.readline

n, i = input().split()
n = int(n)
i = float(i)
all_v = input().split()
res = int(all_v[0])
for k in range(1, n+1):
    v = int(all_v[k]) * (1+i)**(-k)
    # import ipdb; ipdb.set_trace()
    res += v
    

print(res)

# -200*(1+0.05) = -210 
# 100*(1+0.05)**(-1)=95.23809523809524 
# 100 * (1.05)**(-2)=90.702947845804