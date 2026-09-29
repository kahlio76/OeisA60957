# Base case: X, Y disjoint subsets of [2,k], R = prod X * prod Y^2.  A = |Y|.  Gaps of A-values over all R?
import sys, itertools
from collections import defaultdict
k0, k1 = int(sys.argv[1]), int(sys.argv[2])
for k in range(k0, k1 + 1):
    vals = defaultdict(set)
    # enumerate assignments of each s in [2,k] to {0: unused, 1: X, 2: Y}
    items = list(range(2, k + 1))
    def rec(i, R, a):
        if i == len(items): vals[R].add(a); return
        s = items[i]
        rec(i + 1, R, a); rec(i + 1, R * s, a); rec(i + 1, R * s * s, a + 1)
    rec(0, 1, 0)
    bad = [(R, sorted(v)) for R, v in vals.items() if any(b - a > 2 for a, b in zip(sorted(v), sorted(v)[1:]))]
    g2 = sum(1 for v in vals.values() if any(b - a == 2 for a, b in zip(sorted(v), sorted(v)[1:])))
    print('k', k, 'products', len(vals), 'gap>2', len(bad), 'gap==2', g2, bad[:3], flush=True)
