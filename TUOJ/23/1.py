import sys
n = input()
b_list = sys.stdin.readline().split()
max_res = int(b_list[0])
min_res = int(b_list[0])
a_max = int(b_list[0])
for i in range(1, len(b_list)):
    max_res += int(b_list[i])

    if int(b_list[i]) > a_max:
        a_max = int(b_list[i])
        min_res += int(b_list[i])

print(max_res)
print(min_res)
    

