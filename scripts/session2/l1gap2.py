# L=1: A(g) = # small r with g_r = 2.  (i) Do achieved A-values of reps of R have gaps <= 2?
# (ii) For rep f with A(f)=a > min A: distance to nearest rep with A in {a-1, a-2}; worst case per n.
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of
N0, N1, REPMAX = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n or n // p < 2: continue
        k = n // p; W = [s for s in range(2, n + 1) if s % p]
        cap = caps_for(W, p, n); S = suffix_sets(W, cap)
        st = Counter(); dist = Counter(); worst = None
        for R in S[0]:
            reps = all_reps_of(R, W, cap, S)
            if len(reps) < 2 or len(reps) > REPMAX: st['skip'] += len(reps) > REPMAX; continue
            A = [sum(1 for i, c in enumerate(g) if c == 2) for g in reps]
            vals = sorted(set(A))
            g2 = [b - a for a, b in zip(vals, vals[1:])]
            if any(x == 2 for x in g2): st['GAP2'] += 1
            if any(x > 2 for x in g2): st['AGAP'] += 1
            mA = vals[0]
            byA = {}
            for g, a in zip(reps, A): byA.setdefault(a, []).append(g)
            continue
            for f, a in zip(reps, A):
                if a == mA: continue
                cand = byA.get(a - 1, []) + byA.get(a - 2, [])
                d = min(sum(abs(x - y) for x, y in zip(f, g)) for g in cand)
                dist[d] += 1
                if worst is None or d > worst[0]: worst = (d, R, {W[i]: c for i, c in enumerate(f) if c})
        print('n', n, 'p', p, dict(st), dict(sorted(dist.items())), worst, flush=True)
