# Generalized (L*): in class-C world V = p-free [2, X) (caps from n), for ANY composite y coprime to p
# (not only the next element), is every y-fiber {e : N y^e in S(V)} an interval?
# Reports failures by category: y < X (y in V), y == next element, y > next element.
import sys
from collections import Counter
from sympy import primerange, isprime
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
YMULT = int(sys.argv[3]) if len(sys.argv) > 3 else 3
SMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 400000
st = Counter(); shown = Counter()
for X in range(5, XMAX + 1):
    for p in primerange(2, NMAX + 1):
        W = [s for s in range(2, X) if s % p]
        if len(W) < 2: continue
        nxt = X
        while nxt % p == 0: nxt += 1
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if X <= s * p**k <= NMAX) | {X})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            SS = S[0]
            if len(SS) > SMAX: st['skip'] += 1; continue
            st['worlds'] += 1
            maxS = max(SS)
            for y in range(4, YMULT * X + 1):
                if y % p == 0 or isprime(y): continue
                cat = 'inV' if y < X else ('next' if y == nxt else 'beyond')
                for N in SS:
                    if N % y == 0 and (N // y) in SS: continue  # only start fibers at a bottom point... (not needed, cheap filter)
                    # walk up the fiber from N
                    e = 1; gap = False; v = N
                    while True:
                        v *= y
                        if v > maxS: break
                        if v in SS:
                            if gap:
                                st['FAIL_' + cat] += 1
                                if shown[cat, X] < 2:
                                    shown[cat, X] += 1
                                    print('FAIL', cat, 'X', X, 'p', p, 'n', n, 'y', y, 'N', N, 'e', e, flush=True)
                                break
                        else:
                            if gap: pass
                            gap = True
                        e += 1
                    st['fib_' + cat] += 1
    print('X', X, dict(st), flush=True)
