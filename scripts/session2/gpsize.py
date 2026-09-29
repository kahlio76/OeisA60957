# Geodesic property: for each non-M-adjacent pair e,f of reps of N (sub-world V = p-free s in [2,m], caps from n),
# find the minimal size |e'-e| (or |f'-f|) of an M-move that strictly reduces |f-e|. Report distribution + examples.
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of
from lexascent_lib import madj

MMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
REPCAP = int(sys.argv[3]) if len(sys.argv) > 3 else 200
st = Counter(); sizes = Counter(); ex = {}
def dist(a, b): return sum(abs(i - j) for i, j in zip(a, b))
for m in range(4, MMAX + 1):
    for p in primerange(2, NMAX + 1):
        V = [s for s in range(2, m + 1) if s % p]
        if len(V) < 3: continue
        th = sorted(set(s * p**k for s in V for k in range(0, 40) if m <= s * p**k <= NMAX) | {m})
        seen = set()
        for n in th:
            cap = caps_for(V, p, n)
            key = tuple(cap[s] for s in V)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(V, cap)
            if len(S[0]) > 300000: continue
            for N in S[0]:
                R = all_reps_of(N, V, cap, S)
                if len(R) < 2 or len(R) > REPCAP: continue
                for i, e in enumerate(R):
                    for f in R[i + 1:]:
                        if madj(e, f): continue
                        st['pairs'] += 1
                        d = dist(e, f)
                        best = None
                        for g in R:
                            if g != e and madj(e, g) and dist(g, f) < d:
                                s_ = dist(e, g)
                                if best is None or s_ < best: best = s_
                            if g != f and madj(f, g) and dist(e, g) < d:
                                s_ = dist(f, g)
                                if best is None or s_ < best: best = s_
                        if best is None:
                            st['STUCK'] += 1; continue
                        sizes[best] += 1
                        if best >= 5 and len(ex.setdefault(best, [])) < 3:
                            ex[best].append((m, p, n, N, {V[k]: c for k, c in enumerate(e) if c}, {V[k]: f[k] - e[k] for k in range(len(V)) if f[k] != e[k]}))
    print('m', m, dict(st), 'min shortening-move sizes', dict(sorted(sizes.items())), flush=True)
for k, L in sorted(ex.items()):
    for e_ in L: print('EX size', k, e_)
