import sys
input = sys.stdin.readline

n, m = map(int, input().split())
ref = input().split()
ref.insert(0, '-1')
t = input().split()
t.insert(0, '-1')
print_end = True

begin = [0]*(m+1)
end = [0]*(m+1)
succ = [[] for _ in range(m+1)]

def find_ref(idx):
    global print_end
    if int(ref[idx]) == 0:
        begin[idx] = 1
        end[idx] = n - int(t[idx])+1
        if end[idx] <= 0:
            print_end = False
        return True
    else:
        find_ref(int(ref[idx]))
        begin[idx] = begin[int(ref[idx])] + int(t[int(ref[idx])])
        end[idx] = n - int(t[idx])+1
        if end[idx] <= 0 or end[idx] < begin[idx]:
            print_end = False
        


for i in range(1, m+1):
    find_ref(i)
    if int(ref[i]) != 0:
        p = int(ref[i])
        succ[p].append(i)

if print_end:
    for i in range(m, 0, -1):
        for j in succ[i]:
            end[i] = min(end[i], end[j] - int(t[i]))
for i in range(1, m+1):
    if begin[i] > end[i]:
        print_end = False
        break

begin_str = str(begin[1])
end_str = str(end[1])
for j in range(2, len(begin)):
    begin_str = begin_str + ' ' + str(begin[j])
    end_str = end_str + ' ' + str(end[j])
if print_end:
    print(begin_str)
    print(end_str)
else:
    print(begin_str)

