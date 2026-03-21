import sys
input = sys.stdin.readline

start = input().strip() # .strip() 去掉\n
n = int(input())

f = {}
for i in range(n):
    origin = input().strip()
    x, y = origin[1], origin[2]
    f[x] = y
m = int(input())

query = list(map(int,input().split()))

def transform(s):
    new_s = ""
    for idx in range(len(s)):
        char = s[idx]
        char_new = f.get(char, char)
        new_s += char_new
    assert len(new_s) == len(s)
    return new_s



res = []
res.append(start)
for i in range(1, 100+2):
    res_i = transform(res[i-1])
    if res_i.endswith('\n'):
        res_i = res_i[:-1]
    res.append(res_i)

for i in range(m):
    # import ipdb;ipdb.set_trace()
    print(res[query[i]])