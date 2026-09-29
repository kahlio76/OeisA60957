# Greedy-bridge test: for bridge instances (N, N*x in S), is there a rep X of N*x with X - Q M-adjacent
# (as a bridge: X - Q = U+ - U-, each side at most one element of multiplicity >= 2), where Q = greedy-small rep of N?
# Also record minimal shapes. Uses full rep enumeration of N*x only (fast enough for small n).
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from common import caps_real, all_reps
from sigreedy_lib import suffix_sets, greedy_rep
from lexascent_lib import madj

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
st = Counter(); shapes = Counter(); ex = {}
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        for x in range(4, n + 1):
            if x % p == 0 or isprime(x):
                continue
            W, cap = caps_real(n, p, x)
            S = suffix_sets(W, cap)
            reps = all_reps(W, cap)
            for N in S[0]:
                if N * x not in reps:
                    continue
                st['inst'] += 1
                Q = greedy_rep(N, W, cap, S)
                best = None
                for X in reps[N * x]:
                    if madj(Q, X):
                        d = sum(abs(a - b) for a, b in zip(Q, X))
                        if best is None or d < best[0]:
                            best = (d, X)
                if best is None:
                    st['FAIL'] += 1
                    if st['FAIL'] <= 10:
                        print('FAIL', n, p, x, N, {W[i]: c for i, c in enumerate(Q) if c}, flush=True)
                    continue
                d, X = best
                rem = tuple(sorted((W[i], Q[i] - X[i]) for i in range(len(W)) if Q[i] > X[i]))
                add = tuple(sorted((W[i], X[i] - Q[i]) for i in range(len(W)) if X[i] > Q[i]))
                sh = (sum(c for _, c in rem), sum(c for _, c in add))
                shapes[sh] += 1
                if len(ex.setdefault(sh, [])) < 3:
                    ex[sh].append((n, p, x, N, {W[i]: c for i, c in enumerate(Q) if c}, rem, add))
    print('n', n, dict(st), dict(sorted(shapes.items())), flush=True)
for sh, L in sorted(ex.items()):
    print('shape', sh)
    for x in L: print('   ', x)
