import sys
n, k = sys.stdin.readline().split()
n, k = int(n), int(k)
left = [False] * (n+1)
left[0] = True
right = []
counter = 0
for i in range(k):
    left_i, right_i = sys.stdin.readline().split()
    left_i, right_i = int(left_i), int(right_i)
    if left[right_i] == False:
        counter += 1
    left[left_i] = True

print(counter)