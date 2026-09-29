# Local minimality test for bridge pairs.
# A pair (Q,X) in R(N) x R(Nx) is "k-locally minimal" if no ratio-1 move on Q (within R(N)) or on X (within R(Nx))
# that changes at most k block-copies in total (|removed|+|added| <= k) strictly reduces |X-Q|_1.
# Report locally minimal pairs that are NOT M-adjacent, or have |D-| >= 2, for x with given structure.
import sys
from collections import Counter
from itertools import combinations
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of, madj

XMAX, NMAX, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
PAIRMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
only_semi = len(sys.argv) > 5 and sys.argv[5] == 'semi'
st = Counter()

def dist(a, b): return sum(abs(i - j) for i, j in zip(a, b))

for x in range(4, XMAX + 1):
    if isprime(x): continue
    F = factorint(x)
    if only_semi and not (len(F) == 2 and all(v == 1 for v in F.values())): continue
    for p in primerange(2, NMAX + 1):
        if x % p == 0: continue
        W = [s for s in range(2, x) if s % p]
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 500000: continue
            for N in S[0]:
                if N * x not in S[0]: continue
                RN = all_reps_of(N, W, cap, S); RX = all_reps_of(N * x, W, cap, S)
                if len(RN) * len(RX) > PAIRMAX: continue
                # neighbours within the same class via small moves: two reps of the same product at distance <= K
                nbN = {Q: [Q2 for Q2 in RN if Q2 != Q and dist(Q, Q2) <= K] for Q in RN}
                nbX = {X: [X2 for X2 in RX if X2 != X and dist(X, X2) <= K] for X in RX}
                for Q in RN:
                    for X in RX:
                        d = dist(Q, X)
                        if any(dist(Q2, X) < d for Q2 in nbN[Q]) or any(dist(Q, X2) < d for X2 in nbX[X]):
                            continue
                        st['locmin'] += 1
                        dm = sum(max(0, a - b) for a, b in zip(Q, X))
                        m = madj(Q, X)
                        if not m or dm >= 2:
                            st['locmin_bad' if not m else 'locmin_Dminus>=2_but_madj'] += 1
                            if st['locmin_bad'] + st['locmin_Dminus>=2_but_madj'] <= 12:
                                print('LOCMIN', 'madj' if m else 'NOT-MADJ', 'x', x, 'p', p, 'n', n, 'N', N,
                                      'Q', {W[i]: c for i, c in enumerate(Q) if c},
                                      'D', {W[i]: X[i] - Q[i] for i in range(len(W)) if X[i] != Q[i]}, flush=True)
    print('x', x, dict(st), flush=True)
