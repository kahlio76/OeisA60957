# Prefix induction for p^2 > n, k = n//p: add values m = 2, 3, ..., n in order (p-free only).
# m <= k is added twice: step 'a' (cap 0 -> 1) then step 'b' (cap 1 -> 2); m > k: step 'a' only.
# World before a step = all p-free values < m with final caps (2 if <= k), plus m with its current cap.
# Bridge at each step: reps using the new copy vs not; need pair with |dA| <= 2. Report failures + distances;
# also Doubling (gap<=2) in every prefix world.
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of
N0, N1, REPMAX, SHOW = map(int, sys.argv[1:5])
def A(g, W, k): return sum(1 for i, c in enumerate(g) if c == 2 and W[i] <= k)
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n or n // p < 2: continue
        k = n // p; st = Counter(); dist = Counter(); shown = 0
        for m in range(2, n + 1):
            if m % p == 0: continue
            for step, c in (('a', 1), ('b', 2)) if m <= k else (('a', 1),):
                W = [v for v in range(2, m + 1) if v % p]
                cap = {v: (2 if v <= k else 1) for v in W if v < m}; cap[m] = c
                S = suffix_sets(W, cap); it = W.index(m)
                for R in S[0]:
                    reps = all_reps_of(R, W, cap, S)
                    if len(reps) > REPMAX: continue
                    vals = sorted({A(g, W, k) for g in reps})
                    if any(b - a > 2 for a, b in zip(vals, vals[1:])): st['GAP'] += 1
                    new = [g for g in reps if g[it] == c]; old = [g for g in reps if g[it] < c]
                    if not new or not old: continue
                    st[step] += 1
                    best = min((sum(abs(x - y) for x, y in zip(g, h)) for g in new for h in old
                                if abs(A(g, W, k) - A(h, W, k)) <= 2), default=None)
                    if best is None: st['FAIL'] += 1; continue
                    dist[step, best] += 1
                    if best > 3 and shown < SHOW:
                        shown += 1; print('  hard', step, 'm', m, 'R', R, 'd', best, flush=True)
        print('n', n, 'p', p, 'k', k, dict(st), dict(sorted(dist.items())), flush=True)
