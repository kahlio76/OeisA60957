# Is the (a,b)-slice F (fixed {a,b}-free content) CONVEX (= lattice points of its convex hull)?
# World: framework-B V = p-free s < x, caps from n (profile scan), x = a*b semiprime (mode 'semi')
# or general two-prime x (mode 'two').  Also report convexity of column boundary functions L (min b), Hmax (max b).
import sys
from collections import Counter, defaultdict
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for

XMAX, NMAX, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
st = Counter()

def is_convex_lattice(pts):
    """pts: set of (i,j). Check pts == Z^2 ∩ conv(pts) via: columns are intervals, lower boundary convex,
    upper boundary concave (as functions of i over a contiguous i-range)."""
    cols = defaultdict(list)
    for i, j in pts: cols[i].append(j)
    ks = sorted(cols)
    if ks != list(range(ks[0], ks[-1] + 1)): return 'col-gap'
    lo = {}; hi = {}
    for i in ks:
        c = sorted(cols[i])
        if c != list(range(c[0], c[-1] + 1)): return 'col-hole'
        lo[i], hi[i] = c[0], c[-1]
    # discrete convexity of lo and concavity of hi is necessary but for exact lattice-convexity we check
    # the hull: every lattice point in the hull of the columns' endpoints must be in pts.
    for i in ks[1:-1]:
        if lo[i - 1] + lo[i + 1] < 2 * lo[i]: return 'lo-not-convex'
        if hi[i - 1] + hi[i + 1] > 2 * hi[i]: return 'hi-not-concave'
    # full check against convex hull (small sets): for any two points, lattice points on the segment
    P = sorted(pts)
    S = set(pts)
    if len(P) <= 60:
        from math import gcd
        for x1, y1 in P:
            for x2, y2 in P:
                if (x2, y2) <= (x1, y1): continue
                g = gcd(abs(x2 - x1), abs(y2 - y1))
                for s in range(1, g):
                    if (x1 + (x2 - x1) * s // g, y1 + (y2 - y1) * s // g) not in S: return 'segment-hole'
    return 'ok'

for x in range(6, XMAX + 1):
    F_ = factorint(x)
    if len(F_) != 2: continue
    if mode == 'semi' and not all(v == 1 for v in F_.values()): continue
    a, b = sorted(F_)
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
            if len(S[0]) > 2000000: st['skip'] += 1; continue
            groups = defaultdict(set)
            for N in S[0]:
                u = N; ea = eb = 0
                while u % a == 0: u //= a; ea += 1
                while u % b == 0: u //= b; eb += 1
                groups[u].add((ea, eb))
            for NO, pts in groups.items():
                r = is_convex_lattice(pts)
                st[r] += 1
                if r != 'ok' and st[r] <= 3:
                    print('NONCONVEX', r, 'x', x, 'p', p, 'n', n, 'NO', NO, sorted(pts)[:40], flush=True)
    print('x', x, dict(st), flush=True)
