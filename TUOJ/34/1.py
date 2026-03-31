import sys
input = sys.stdin.readline

n, m, p, q = map(int, input().split())
all_nums = []
for i in range(n):
    row = list(input().split())
    all_nums.extend(row)
row_idx = 0
for i in range(p):
    new_row = all_nums[row_idx:row_idx+q]
    row_idx += q
    print(' '.join(new_row))
        
