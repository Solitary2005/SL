# import sys
# input = sys.stdin.readline

# n, m = map(int, input().split())
# a = list(map(int, input().split()))

# S = []
# size_S = []
# a_s = []

# for i in range(m):
#     s_i = list(map(int, input().split()))
#     size_i = s_i.pop(0)
#     S.append(s_i)
#     size_S.append(size_i)

# for i in range(m):
#     t_i = list(map(int, input().split()))
#     size_i = t_i.pop(0)
#     real_ans = "correct"
#     c_ans = "correct"
#     if size_i != size_S[i]:
#         real_ans = "wrong"
#     for j in range(size_i):
#         if size_i == size_S[i]:
#             if t_i[j] != S[i][j]:
#                 real_ans = "wrong"
#         s_c = a[j]
#         t_c = a[j]
#         for item_s, item_t in zip(S[i], t_i):
#             s_c = s_c ^ item_s
#             t_c = t_c ^ item_t
#         if s_c != t_c:
#             c_ans == "wrong"


#         if c_ans == "wrong" and real_ans == "wrong":
#             break
#     if real_ans == c_ans:
#         print("correct")
#     else:
#         print("wrong")
    
import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    S = []
    for _ in range(m):
        size = int(next(it))
        s = [int(next(it)) for _ in range(size)]
        S.append(s)
    out = []
    for i in range(m):
        size = int(next(it))
        t = [int(next(it)) for _ in range(size)]
        s = S[i]
        # 实际是否相等
        real_equal = (len(s) == len(t) and s == t)
        # 计算异或和
        xor_s = 0
        for x in s:
            xor_s ^= a[x-1]
        xor_t = 0
        for x in t:
            xor_t ^= a[x-1]
        c_equal = (xor_s == xor_t)
        out.append("correct" if real_equal == c_equal else "wrong")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()