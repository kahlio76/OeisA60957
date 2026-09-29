# Fully arbitrary: random V subset of [2, M], random caps in {1,2}; A = # cap-2 elements used twice.
import sys, random
from collections import defaultdict
M, TR, SZ = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); random.seed(5)
bad = 0; tot = 0
for tr in range(TR):
    V = random.sample(range(2, M + 1), SZ); cap = {v: random.choice([1, 2]) for v in V}
    vals = defaultdict(set)
    def rec(i, R, a):
        if i == len(V): vals[R].add(a); return
        v = V[i]
        rec(i + 1, R, a); rec(i + 1, R * v, a)
        if cap[v] == 2: rec(i + 1, R * v * v, a + 1)
    rec(0, 1, 0)
    for R, s in vals.items():
        s = sorted(s); tot += 1
        if any(b - a > 2 for a, b in zip(s, s[1:])):
            bad += 1
            if bad <= 5: print('GAP V', sorted((v, cap[v]) for v in V), 'R', R, s, flush=True)
print('products', tot, 'gap>2', bad)
