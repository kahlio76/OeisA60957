# Test "lex-ascent": in the core world of the real problem (p-free s in [2,n], caps = chain lengths),
# every rep e of N that is not lex-max has an M-adjacent rep f of N with f >_lex e.
# Lex order: count vector indexed by increasing s (so lex-max prefers small elements).
# Usage: lexascent.py N0 N1 [order]  order in {small, large}
import sys
from collections import Counter
from sympy import primerange
from common import all_reps

def madj(e, f):
    up = dn = 0
    for a, b in zip(e, f):
        d = b - a
        if d >= 2:
            up += 1
            if up > 1: return False
        elif d <= -2:
            dn += 1
            if dn > 1: return False
    return True

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
order = sys.argv[3] if len(sys.argv) > 3 else 'small'
st = Counter()
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        W = [s for s in range(2, n + 1) if s % p]
        if order == 'large':
            W = W[::-1]
        cap = {}
        for s in W:
            k = 0; v = s
            while v <= n:
                k += 1; v *= p
            cap[s] = k
        reps = all_reps(W, cap)
        for N, lst in reps.items():
            if len(lst) == 1:
                continue
            top = max(lst)
            for e in lst:
                if e == top:
                    continue
                st['nontop'] += 1
                if not any(f > e and madj(e, f) for f in lst):
                    st['STUCK'] += 1
                    if st['STUCK'] <= 15:
                        print('STUCK', n, p, N, {W[i]: c for i, c in enumerate(e) if c},
                              'top', {W[i]: c for i, c in enumerate(top) if c}, flush=True)
    print('n', n, dict(st), flush=True)
