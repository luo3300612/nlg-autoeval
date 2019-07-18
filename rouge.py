import numpy as np


def lcs(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i, j] = dp[i - 1, j - 1] + 1
            else:
                dp[i, j] = max(dp[i - 1, j], dp[i, j - 1])
    print(dp)
    return dp[m, n]


s1 = "you are a big huge duck duck duck duck duck dog dog dog dog dog dog book".split(' ')
s2 = "you a huge dog dog duck duck duck duck duck dog dog dog dog dog dog play take book".split(' ')

print(lcs(s1, s2))
