# General world: smalls 2..k cap 2, larges = random subset Lam of [k+1, M] cap 1 (no p-freeness).
# (i) Doubling gap <= 2 for all R.  (ii) slack bridge when adding x (in [k+1,M], not in Lam):
#     R, R/x both representable over Lam-world -> reps g of R, g' of R/x with |A(g)-A(g')| <= 2; record min distance.
import sys, random
from collections import Counter
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of
K0, K1, MMULT, TR, REPMAX = map(int, sys.argv[1:6]); random.seed(2)
def Aof(g, W, k): return sum(1 for i, c in enumerate(g) if c == 2 and W[i] <= k)
for k in range(K0, K1 + 1):
    M = MMULT * k
    st = Counter(); dist = Counter()
    for tr in range(TR):
        pool = list(range(k + 1, M + 1))
        Lam = set(random.sample(pool, random.randint(0, min(len(pool), 9))))
        W = list(range(2, k + 1)) + sorted(Lam)
        cap = {s: (2 if s <= k else 1) for s in W}
        S = suffix_sets(W, cap)
        for R in S[0]:
            reps = all_reps_of(R, W, cap, S)
            if not reps or len(reps) > REPMAX: continue
            vals = sorted({Aof(g, W, k) for g in reps})
            st['R'] += 1
            if any(b - a > 2 for a, b in zip(vals, vals[1:])):
                st['GAP>2'] += 1
                if st['GAP>2'] <= 3: print('GAP k', k, 'Lam', sorted(Lam), 'R', R, vals, flush=True)
        outs = [x for x in pool if x not in Lam]
        for x in random.sample(outs, min(3, len(outs))):
            for R in S[0]:
                if R % x or (R // x) not in S[0]: continue
                A1 = all_reps_of(R, W, cap, S); A2 = all_reps_of(R // x, W, cap, S)
                if len(A1) * len(A2) > REPMAX * 20: continue
                st['bridge'] += 1
                best = None
                for g in A1:
                    for h in A2:
                        if abs(Aof(g, W, k) - Aof(h, W, k)) <= 2:
                            d = sum(abs(a - b) for a, b in zip(g, h)) + 1
                            best = d if best is None or d < best else best
                if best is None:
                    st['BRIDGE_FAIL'] += 1
                    if st['BRIDGE_FAIL'] <= 3: print('BFAIL k', k, 'x', x, 'Lam', sorted(Lam), 'R', R, flush=True)
                else: dist[best] += 1
    print('k', k, 'M', M, dict(st), 'bridge dist', dict(sorted(dist.items())), flush=True)
