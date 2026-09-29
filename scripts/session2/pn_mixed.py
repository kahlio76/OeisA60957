# P_n = {prod S : S subset [1..n]}.  Directions with mixed signs: ratio r = y/z (gcd 1, z >= 2).
# Is {e in Z : m r^e in P_n} an interval (over all integer e with m r^e integral)?
import sys
from math import gcd
from fractions import Fraction
from collections import Counter
N0, N1 = int(sys.argv[1]), int(sys.argv[2])
RMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 30
for n in range(N0, N1 + 1):
    P = {1}
    for k in range(2, n + 1):
        P |= {v * k for v in P}
    st = Counter()
    for y in range(1, RMAX + 1):
        for z in range(2, RMAX + 1):
            if gcd(y, z) != 1: continue
            # fibers: equivalence classes m ~ m*y/z. Start from m in P with m*z/y not in P or not integral.
            for m in P:
                if (m * z) % y == 0 and (m * z // y) in P: continue
                # walk up: m*(y/z)^e
                v = m; gap = False; e = 0
                while True:
                    if v % z: break
                    v = v // z * y
                    e += 1
                    if v in P:
                        if gap:
                            st['FAIL'] += 1
                            if st['FAIL'] <= 8: print('FAIL n', n, 'y/z', y, z, 'm', m, 'e', e, flush=True)
                            break
                    else:
                        gap = True
                st['fib'] += 1
    print('n', n, '|P|', len(P), dict(st), flush=True)
