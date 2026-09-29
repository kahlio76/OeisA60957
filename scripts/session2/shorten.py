# For bridge instances: for every NON-M-adjacent pair (Q,X) in R(N) x R(Nx), find the smallest ratio-1
# modification (of Q within R(N), or of X within R(Nx)) that strictly reduces |X-Q|_1.
# "size" of a modification Y->Y' = |Y'-Y|_1. Report the max over pairs of the min size needed.
import sys
from collections import Counter
from sympy import isprime, primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of, madj

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
PAIRMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
st = Counter(); worst = Counter(); ex = {}
def dist(a, b): return sum(abs(i - j) for i, j in zip(a, b))
for x in range(4, XMAX + 1):
    if isprime(x):
        continue
    for p in primerange(2, NMAX + 1):
        if x % p == 0:
            continue
        W = [s for s in range(2, x) if s % p]
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen:
                continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 800000:
                continue
            for N in S[0]:
                if N * x not in S[0]:
                    continue
                RN = all_reps_of(N, W, cap, S); RX = all_reps_of(N * x, W, cap, S)
                if len(RN) * len(RX) > PAIRMAX or len(RN) + len(RX) < 3:
                    continue
                for Q in RN:
                    for X in RX:
                        if madj(Q, X):
                            continue
                        st['nonmadj_pairs'] += 1
                        d = dist(Q, X)
                        best = None
                        for Q2 in RN:
                            if dist(Q2, X) < d:
                                s = dist(Q, Q2)
                                if best is None or s < best[0]: best = (s, 'Q', Q2)
                        for X2 in RX:
                            if dist(Q, X2) < d:
                                s = dist(X, X2)
                                if best is None or s < best[0]: best = (s, 'X', X2)
                        worst[best[0]] += 1
                        if best[0] >= 5 and len(ex.setdefault(best[0], [])) < 3:
                            ex[best[0]].append((x, p, n, N, {W[i]: c for i, c in enumerate(Q) if c}, {W[i]: c for i, c in enumerate(X) if c}, best[1],
                                                {W[i]: best[2][i] - (Q if best[1] == 'Q' else X)[i] for i in range(len(W)) if best[2][i] != (Q if best[1] == 'Q' else X)[i]}))
    print('x', x, dict(st), 'min-shortening-size distribution', dict(sorted(worst.items())), flush=True)
for k, L in sorted(ex.items()):
    print('size', k)
    for e in L: print('   ', e)
