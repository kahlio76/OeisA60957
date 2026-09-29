# Fixed n, p (p^2 > n), k = n//p.  Class world C(j, M): smalls [2..j] cap 2, M subset (j,k] cap 1, all p-free (k,n] cap 1.
# (Ba) x in (j,k] \ M: R, R/x representable in C(j,M) -> pair (g of R, h of R/x) with |A(g)-A(h)| <= 2.
# (Bb) j+1 in M: in world C(j+1, M-{j+1}) reps with g_{j+1}=2 and reps with g_{j+1}<=1 -> pair within 2.
# Record failures and minimal witness distance (in the larger world).
import sys, itertools
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of
N0, N1, REPMAX = map(int, sys.argv[1:4])
def world(n, p, k, j, M):
    W = list(range(2, j + 1)) + sorted(M) + [s for s in range(k + 1, n + 1) if s % p]
    cap = {s: (2 if s <= j else 1) for s in W}
    return W, cap
def A(g, W, j): return sum(1 for i, c in enumerate(g) if c == 2 and W[i] <= j)
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n or n // p < 2: continue
        k = n // p; st = Counter(); dist = Counter()
        for j in range(1, k + 1):
            mids = list(range(j + 1, k + 1))
            for m in range(len(mids) + 1):
                for M in itertools.combinations(mids, m):
                    # (Bb) world C(j, M) with j+1 in M, promoted to C(j+1, M - {j+1})
                    if j + 1 in M:
                        W, cap = world(n, p, k, j + 1, set(M) - {j + 1}); S = suffix_sets(W, cap); it = W.index(j + 1)
                        for R in S[0]:
                            reps = all_reps_of(R, W, cap, S)
                            if len(reps) > REPMAX: continue
                            new = [g for g in reps if g[it] == 2]; old = [g for g in reps if g[it] < 2]
                            if not new or not old: continue
                            st['Bb'] += 1
                            best = min((sum(abs(a - b) for a, b in zip(g, h)) for g in new for h in old
                                        if abs(A(g, W, j + 1) - A(h, W, j + 1)) <= 2), default=None)
                            if best is None: st['Bb_FAIL'] += 1; print('BbFAIL', n, p, j, M, R, flush=True)
                            else: dist['b', best] += 1
                    # (Ba) add x in (j,k] \ M
                    for x in mids:
                        if x in M: continue
                        W, cap = world(n, p, k, j, set(M) | {x}); S = suffix_sets(W, cap); it = W.index(x)
                        for R in S[0]:
                            reps = all_reps_of(R, W, cap, S)
                            if len(reps) > REPMAX: continue
                            new = [g for g in reps if g[it] == 1]; old = [g for g in reps if g[it] == 0]
                            if not new or not old: continue
                            st['Ba'] += 1
                            best = min((sum(abs(a - b) for a, b in zip(g, h)) for g in new for h in old
                                        if abs(A(g, W, j) - A(h, W, j)) <= 2), default=None)
                            if best is None: st['Ba_FAIL'] += 1; print('BaFAIL', n, p, j, M, x, R, flush=True)
                            else: dist['a', best] += 1
        print('n', n, 'p', p, 'k', k, dict(st), dict(sorted(dist.items())), flush=True)
