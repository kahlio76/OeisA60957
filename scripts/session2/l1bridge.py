# Induction on n for the Doubling Lemma (p^2 > n). At step n the reps of R over W_n split into
# old side (not using the new item) and new side (using it). Need a pair (old, new) with |dA| <= 2.
# Report: failures, and the minimal l1 distance of such a pair (max over R).
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of
N0, N1, REPMAX = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n or n % p == 0 and n // p < 2: continue
        if n % p and n % p == 0: pass
        k = n // p
        W = [s for s in range(2, n + 1) if s % p]
        cap = caps_for(W, p, n); S = suffix_sets(W, cap)
        if n % p:   # new large value x = n (cap 1): new side = reps with g_n = 1
            item = W.index(n); lim = 1; kind = 'a'
        else:       # n = kp: new side = reps with g_k = 2
            if k not in W: continue
            item = W.index(k); lim = 2; kind = 'b'
        st = Counter(); dist = Counter(); worst = None
        for R in S[0]:
            reps = all_reps_of(R, W, cap, S)
            if len(reps) > REPMAX: st['skip'] += 1; continue
            new = [g for g in reps if g[item] == lim]; old = [g for g in reps if g[item] < lim]
            if not new or not old: continue
            st['inst'] += 1
            A = lambda g: sum(1 for i, c in enumerate(g) if c == 2)
            best = None
            for g in new:
                for h in old:
                    if abs(A(g) - A(h)) <= 2:
                        d = sum(abs(x - y) for x, y in zip(g, h))
                        if best is None or d < best: best = d
            if best is None: st['FAIL'] += 1; continue
            dist[best] += 1
            if worst is None or best > worst[0]: worst = (best, R)
        print('n', n, 'p', p, kind, dict(st), dict(sorted(dist.items())), worst, flush=True)
