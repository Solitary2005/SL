import sys
input = sys.stdin.readline

n, m = map(int, input().split())
article_counter = {}
counter = {}

for i in range(n):
    article = list(map(int, input().split()))
    see_in_article = [False] * (max(article)+1)
    for j in range(1, len(article)):
        word = article[j]
        counter_j = counter.get(word, 0)
        counter[word] = counter_j + 1
        if not see_in_article[word]:
            article_counter_j = article_counter.get(word, 0)
            article_counter[word] = article_counter_j + 1
            see_in_article[word] = True

for o in range(1, m+1):
    res = [str(article_counter[o]), str(counter[o])]
    print(" ".join(res))