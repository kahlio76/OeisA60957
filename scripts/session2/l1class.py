# Induction class for p^2 > n: smalls [2..j] cap 2; middle values (j, k] present as an arbitrary subset, cap 1;
# all p-free values in (k, n] cap 1  (k = n//p, j <= k).  Test Doubling (gap <= 2) exhaustively over subsets.
import sys, itertools
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of
N0, N1, REPMAX = map(int, sys.argv[1:4])
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n or n // p < 2: continue
        k = n // p; st = Counter()
        for j in range(1, k + 1):
            mids = list(range(j + 1, k + 1))
            for m in range(len(mids) + 1):
                for Mset in itertools.combinations(mids, m):
                    W = list(range(2, j + 1)) + list(Mset) + [s for s in range(k + 1, n + 1) if s % p]
                    cap = {s: (2 if s <= j else 1) for s in W}
                    S = suffix_sets(W, cap)
                    for R in S[0]:
                        reps = all_reps_of(R, W, cap, S)
                        if len(reps) < 2 or len(reps) > REPMAX: continue
                        vals = sorted({sum(1 for i, c in enumerate(g) if c == 2) for g in reps})
                        st['R'] += 1
                        if any(b - a > 2 for a, b in zip(vals, vals[1:])):
                            st['GAP>2'] += 1
                            if st['GAP>2'] <= 2: print('GAP n', n, 'p', p, 'j', j, 'mid', Mset, 'R', R, vals, flush=True)
        print('n', n, 'p', p, 'k', k, dict(st), flush=True)
