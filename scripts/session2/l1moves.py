# Prefix induction, step adding a copy of m. new = reps using the new copy (g_m = c), old = the rest.
# Classify which local move types connect new/old with |dA| <= 2:
#  S3: old = new - [m] + [u] + [v]           (split m, uv = m)
#  W4: old = new - [m] - [a] + [b] + [c]     (swap, m a = b c)
# Check coverage over all instances; print uncovered.
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of
N0, N1, REPMAX = map(int, sys.argv[1:4])
def A(g, W, k): return sum(1 for i, c in enumerate(g) if c == 2 and W[i] <= k)
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n or n // p < 2: continue
        k = n // p; st = Counter()
        for m in range(2, n + 1):
            if m % p == 0: continue
            for step, c in (('a', 1), ('b', 2)) if m <= k else (('a', 1),):
                W = [v for v in range(2, m + 1) if v % p]
                cap = {v: (2 if v <= k else 1) for v in W if v < m}; cap[m] = c
                S = suffix_sets(W, cap); it = W.index(m)
                for R in S[0]:
                    reps = all_reps_of(R, W, cap, S)
                    if len(reps) > REPMAX: continue
                    new = [g for g in reps if g[it] == c]; old = set(g for g in reps if g[it] < c)
                    if not new or not old: continue
                    st['inst'] += 1
                    kinds = set()
                    for g in new:
                        for h in old:
                            if abs(A(g, W, k) - A(h, W, k)) > 2: continue
                            d = [h[i] - g[i] for i in range(len(W))]
                            if sum(abs(x) for x in d) == 3: kinds.add('S3')
                            elif sum(abs(x) for x in d) == 4: kinds.add('W4')
                    st['S3' if 'S3' in kinds else ('W4' if 'W4' in kinds else 'NONE')] += 1
                    if not kinds: print('UNCOVERED n', n, 'p', p, 'm', m, step, 'R', R, flush=True)
        print('n', n, 'p', p, dict(st), flush=True)
