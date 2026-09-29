# Test UP_w: world V = p-free s in [2,w] with caps from n (c_s = #{i: s p^i <= n}).
# For every N and rep e of N with e_w < max_h h_w, exists rep f of N, M-adjacent to e, with f_w > e_w.
# Also record the minimal move shapes.
import sys
from collections import Counter
from sympy import primerange, isprime
from common import all_reps
from lexascent_lib import madj

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
st = Counter(); shapes = Counter(); ex = {}
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        for w in range(4, n + 1):
            if w % p == 0 or isprime(w):
                continue
            V = [s for s in range(2, w + 1) if s % p]
            cap = {}
            for s in V:
                k = 0; v = s
                while v <= n:
                    k += 1; v *= p
                cap[s] = k
            reps = all_reps(V, cap)
            iw = len(V) - 1
            for N, lst in reps.items():
                mx = max(e[iw] for e in lst)
                for e in lst:
                    if e[iw] == mx:
                        continue
                    st['cases'] += 1
                    best = None
                    for f in lst:
                        if f[iw] > e[iw] and madj(e, f):
                            d = sum(abs(a - b) for a, b in zip(e, f))
                            if best is None or d < best[0]:
                                best = (d, f)
                    if best is None:
                        st['STUCK'] += 1
                        if st['STUCK'] <= 10:
                            print('STUCK', n, p, w, N, {V[i]: c for i, c in enumerate(e) if c}, flush=True)
                        continue
                    d, f = best
                    rem = tuple(sorted((V[i], e[i] - f[i]) for i in range(len(V)) if e[i] > f[i]))
                    add = tuple(sorted((V[i], f[i] - e[i]) for i in range(len(V)) if f[i] > e[i]))
                    sh = (sum(c for _, c in rem), sum(c for _, c in add))
                    shapes[sh] += 1
                    if len(ex.setdefault(sh, [])) < 4:
                        ex[sh].append((n, p, w, N, {V[i]: c for i, c in enumerate(e) if c}, rem, add))
    print('n', n, dict(st), dict(sorted(shapes.items())), flush=True)
for sh, L in sorted(ex.items()):
    if sum(sh) >= 4:
        print('shape', sh)
        for x in L: print('   ', x)
