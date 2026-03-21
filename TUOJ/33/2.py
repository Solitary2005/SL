import sys
input = sys.stdin.readline

n, m = map(int, input().split())
doc_0 = input().lower().split()
doc_0_set = set(doc_0)
doc_1 = input().lower().split()
doc_1_set = set(doc_1)
all_set = set(doc_0 + doc_1)
intwo = 0
for i in doc_0_set:
    if i in doc_1_set:
        intwo += 1

print(intwo)
print(len(all_set))
