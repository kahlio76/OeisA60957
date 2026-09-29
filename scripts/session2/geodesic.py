# Geodesic test for M-connectivity in the core world (p-free s in [2,n], caps = chain lengths l_s):
# For every N and every pair of reps e != f of N that are NOT M-adjacent, is there an M-adjacent rep e'
# of e (or f' of f) with |f - e'| < |f - e| (resp |f' - e| < |f - e|)?
import sys
from collections import Counter
from sympy import primerange
from common import all_reps
from lexascent_lib import madj

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
PAIRCAP = int(sys.argv[3]) if len(sys.argv) > 3 else 400
st = Counter()
def dist(a, b): return sum(abs(i - j) for i, j in zip(a, b))
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        W = [s for s in range(2, n + 1) if s % p]
        cap = {}
        for s in W:
            k = 0; v = s
            while v <= n:
                k += 1; v *= p
            cap[s] = k
        reps = all_reps(W, cap)
        for N, lst in reps.items():
            if len(lst) < 2 or len(lst) > PAIRCAP:
                if len(lst) > PAIRCAP: st['skip'] += 1
                continue
            nbr = {e: [f for f in lst if f != e and madj(e, f)] for e in lst}
            for i, e in enumerate(lst):
                for f in lst[i + 1:]:
                    if madj(e, f):
                        continue
                    st['pairs'] += 1
                    d = dist(e, f)
                    if any(dist(g, f) < d for g in nbr[e]) or any(dist(e, g) < d for g in nbr[f]):
                        continue
                    st['STUCK'] += 1
                    if st['STUCK'] <= 10:
                        print('STUCK', n, p, N, {W[k]: c for k, c in enumerate(e) if c}, {W[k]: c for k, c in enumerate(f) if c}, flush=True)
    print('n', n, dict(st), flush=True)
