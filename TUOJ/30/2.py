import sys
input = sys.stdin.readline

n, d = map(int, input().split())
Q = []
K = []
V = []
for mat in range(3):
    for i in range(n):
        if mat == 0:
            Q.append(input().split())
        elif mat == 1:
            K.append(input().split())
        else:
            V.append(input().split())

W = input().split()

# (W × (Q × Kᵀ)) × V = W × ((Q × Kᵀ) × V) = W × (Q × (Kᵀ × V))
kv_res = []
for i in range(d):
    row = []
    for j in range(d):
        item = 0
        for t in range(n):
            item += int(K[t][i]) * int(V[t][j])
        row.append(item)
    kv_res.append(row)

qkv_res = []
for i in range(n):
    row = []
    for j in range(d):
        item = 0
        for t in range(d):
            item += int(Q[i][t]) * int(kv_res[t][j])
        row.append(item)
    qkv_res.append(row)


for i in range(n):
    row_str = []
    for j in range(d):
        val = int(W[i]) * qkv_res[i][j]
        row_str.append(str(val))
    print(' '.join(row_str))
