import sys
input = sys.stdin.readline

n = int(input())
round_dict = {}
round_counter = [0] * n
for i in range(n):
    round = ""
    for _ in range(8):
        round += input()
    cur_counter = round_dict.get(round, 0)
    round_dict[round] = cur_counter + 1
    round_counter[i] = round_dict[round]

for j in range(n):
    print(round_counter[j])