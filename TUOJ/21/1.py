import sys
def relu(x):
    return max(0, x)

n = int(input())
all_score = 0
for i in range(n):
    w, sc = sys.stdin.readline().split()
    w = int(w)
    sc = int(sc)
    all_score += w * sc

all_score = relu(all_score)
print(all_score)