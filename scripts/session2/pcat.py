# (p-cat): for disjoint D+, D- subsets of [2..n] with prod D+ = p^t prod D-, t >= 2, is there a
# certificate: parts A subset D+, B subset D- (any, incl. empty/full) and 0<k<t with
#   prodA/prodB = p^k   (then (A,B) must be proper automatically), or
#   prodA/prodB = p^k * w^s, s=+-1, w in [2..n] \ (D+ u D-)?
# Exhaustive over all such D for small n.
import sys, itertools
from math import prod
from collections import defaultdict, Counter
from sympy import primerange

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
PS = [int(t) for t in sys.argv[3].split(',')] if len(sys.argv) > 3 else None

def vp(m, p):
    k = 0
    while m % p == 0: m //= p; k += 1
    return k, m

for n in range(N0, N1 + 1):
    elems = list(range(2, n + 1))
    for p in (PS or list(primerange(2, n + 1))):
        if p > n: continue
        # all subsets grouped by p-free part of product
        groups = defaultdict(list)
        for mask in range(1 << len(elems)):
            P = 1
            for i, e in enumerate(elems):
                if mask >> i & 1: P *= e
            a, r = vp(P, p)
            groups[r].append((mask, a))
        st = Counter()
        for r, L in groups.items():
            if len(L) < 2: continue
            for (m1, a1) in L:
                for (m2, a2) in L:
                    if m1 & m2 or a1 - a2 < 2: continue
                    t = a1 - a2
                    Dp = [e for i, e in enumerate(elems) if m1 >> i & 1]
                    Dm = [e for i, e in enumerate(elems) if m2 >> i & 1]
                    supp = set(Dp) | set(Dm)
                    free = [w for w in elems if w not in supp]
                    st['D'] += 1
                    ok = False
                    # enumerate parts
                    for sa in range(1 << len(Dp)):
                        pa = prod(Dp[i] for i in range(len(Dp)) if sa >> i & 1)
                        for sb in range(1 << len(Dm)):
                            pb = prod(Dm[i] for i in range(len(Dm)) if sb >> i & 1)
                            # ratio pa/pb = p^k * w^s ?
                            num, den = pa, pb
                            for k in range(1, t):
                                pk = p ** k
                                # pa = pk*pb  (w absent)
                                if num == pk * den: ok = True; break
                                # pa = pk*w*pb  -> w = pa/(pk*pb)
                                if num % (pk * den) == 0:
                                    w = num // (pk * den)
                                    if 2 <= w <= n and w not in supp: ok = True; break
                                # pa*w = pk*pb -> w = pk*pb/pa
                                if (pk * den) % num == 0:
                                    w = (pk * den) // num
                                    if 2 <= w <= n and w not in supp: ok = True; break
                            if ok: break
                        if ok: break
                    if not ok:
                        st['NOCERT'] += 1
                        if st['NOCERT'] <= 5: print('NOCERT n', n, 'p', p, 't', t, 'D+', Dp, 'D-', Dm, flush=True)
        print('n', n, 'p', p, dict(st), flush=True)
