# Doubling Lemma in worlds: smalls [2..k] cap 2 (k = n//p), larges = random subset of p-free (k, n] cap 1.
import sys, random
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of
N0, N1, TR, REPMAX = map(int, sys.argv[1:5]); random.seed(1)
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if p * p <= n or n // p < 2: continue
        k = n // p
        smalls = list(range(2, k + 1)); larges = [s for s in range(k + 1, n + 1) if s % p]
        st = Counter()
        for tr in range(TR):
            dele = set(random.sample(larges, random.randint(1, min(4, len(larges)))))
            W = smalls + [x for x in larges if x not in dele]
            cap = {s: (2 if s <= k else 1) for s in W}
            S = suffix_sets(W, cap)
            for R in S[0]:
                reps = all_reps_of(R, W, cap, S)
                if len(reps) < 2 or len(reps) > REPMAX: continue
                vals = sorted({sum(1 for c in g if c == 2) for g in reps})
                st['R'] += 1
                if any(b - a > 2 for a, b in zip(vals, vals[1:])):
                    st['GAP>2'] += 1
                    if st['GAP>2'] <= 3: print('GAP n', n, 'p', p, 'deleted', sorted(dele), 'R', R, vals, flush=True)
        print('n', n, 'p', p, dict(st), flush=True)
