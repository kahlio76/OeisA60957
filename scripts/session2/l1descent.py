# L = 1 (p <= n < p^2). Reps g of R over W_n (p-free numbers <= n, cap 2 if r <= k=n//p else 1).
# A(g) = #{r: g_r = 2}, B(g) = #{r <= k: g_r >= 1} + 1.  E_n(R) = union [A,B].
# Descent test: for every rep f with A(f) > min A, is there g with A(g) < A(f) and B(g) >= A(f) - 1 ?
# Stronger: g with A(g) = A(f) - 1, B(g) >= B(f) - 1.  Record minimal |g - f| for the strong version.
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of
N0, N1 = int(sys.argv[1]), int(sys.argv[2]); REPMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n: continue
        k = n // p
        W = [s for s in range(2, n + 1) if s % p]
        cap = caps_for(W, p, n)
        S = suffix_sets(W, cap)
        st = Counter(); dist = Counter(); ex = []
        for R in S[0]:
            reps = all_reps_of(R, W, cap, S)
            if len(reps) < 2 or len(reps) > REPMAX: continue
            AB = [(sum(1 for c in g if c == 2), sum(1 for i, c in enumerate(g) if W[i] <= k and c >= 1) + 1) for g in reps]
            mA = min(a for a, b in AB)
            for fi, f in enumerate(reps):
                a, b = AB[fi]
                if a == mA: continue
                st['f'] += 1
                if not any(AB[gi][0] < a and AB[gi][1] >= a - 1 for gi in range(len(reps))):
                    st['WEAK_FAIL'] += 1
                best = None
                for gi, g in enumerate(reps):
                    if AB[gi][0] == a - 1 and AB[gi][1] >= b - 1:
                        d = sum(abs(x - y) for x, y in zip(f, g))
                        if best is None or d < best: best = d
                if best is None:
                    st['STRONG_FAIL'] += 1
                    if len(ex) < 3: ex.append((R, {W[i]: c for i, c in enumerate(f) if c}))
                else: dist[best] += 1
        print('n', n, 'p', p, dict(st), 'dist', dict(sorted(dist.items())), ex[:2], flush=True)
