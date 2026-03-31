import sys
input = sys.stdin.readline

def reshape(ori_mat, p, q):
    num_rows = len(ori_mat)
    all_nums = []
    for i in range(num_rows):
        all_nums.extend(ori_mat[i])
    new_mat = []
    row_idx = 0
    for i in range(p):
        new_row = all_nums[row_idx:row_idx+q]
        row_idx += q
        new_mat.append(new_row)
    return new_mat

def transform(ori_mat):
    num_rows = len(ori_mat)
    num_cols = len(ori_mat[0])
    new_mat = [[0] * num_rows for _ in range(num_cols)]
    for i in range(num_rows):
        for j in range(num_cols):
            new_mat[j][i] = ori_mat[i][j]
    return new_mat

def query(mat, i, j):
    return mat[i][j]

n, m, t = map(int, input().split())
mat = []
for i in range(n):
    row = list(input().split())
    mat.append(row)

for q in range(t):
    op, a, b = map(int, input().split())
    if op == 1:
        mat = reshape(mat, a, b)
    if op == 2:
        mat = transform(mat)
    if op == 3:
        res = query(mat, a, b)
        print(res)