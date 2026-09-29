# Original setting: P_n = {prod S : S subset [1..n]}.  Is {e : m y^e in P_n} an interval for EVERY y >= 2 (not only primes)?
import sys
from collections import Counter
N0, N1 = int(sys.argv[1]), int(sys.argv[2])
YMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 200
for n in range(N0, N1 + 1):
    P = {1}
    for k in range(2, n + 1):
        P |= {v * k for v in P}
    mx = max(P)
    st = Counter()
    for y in range(2, YMAX + 1):
        for m in P:
            if m % y == 0 and (m // y) in P: continue
            v = m; gap = False
            while True:
                v *= y
                if v > mx: break
                if v in P:
                    if gap:
                        st['FAIL'] += 1
                        if st['FAIL'] <= 5: print('FAIL n', n, 'y', y, 'm', m, flush=True)
                        break
                else:
                    gap = True
            st['fib'] += 1
    print('n', n, '|P|', len(P), dict(st), flush=True)
