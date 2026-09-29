# Geodesic property (GP) on sub-worlds V = p-free s in [2, m] with caps from n >= m (all distinct cap profiles).
# For every N and non-M-adjacent pair e,f in R(N): exists M-neighbour of e or f (in R(N)) strictly closer.
# Enumerates reps via suffix sets; skips classes with too many reps.
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of
from lexascent_lib import madj

MMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
REPCAP = int(sys.argv[3]) if len(sys.argv) > 3 else 300
SMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 400000
st = Counter()
def dist(a, b): return sum(abs(i - j) for i, j in zip(a, b))
for m in range(4, MMAX + 1):
    for p in primerange(2, NMAX + 1):
        V = [s for s in range(2, m + 1) if s % p]
        if len(V) < 3:
            continue
        th = sorted(set(s * p**k for s in V for k in range(0, 40) if m <= s * p**k <= NMAX) | {m})
        seen = set()
        for n in th:
            cap = caps_for(V, p, n)
            key = tuple(cap[s] for s in V)
            if key in seen:
                continue
            seen.add(key)
            S = suffix_sets(V, cap)
            if len(S[0]) > SMAX:
                st['skip_big'] += 1; continue
            st['worlds'] += 1
            # only classes N with >=2 reps: detect quickly by enumerating reps for all N is too slow;
            # enumerate reps per N lazily with a cap
            for N in S[0]:
                R = all_reps_of(N, V, cap, S)
                if len(R) < 2:
                    continue
                if len(R) > REPCAP:
                    st['skip_class'] += 1; continue
                nbr = {e: [f for f in R if f != e and madj(e, f)] for e in R}
                for i, e in enumerate(R):
                    for f in R[i + 1:]:
                        if madj(e, f):
                            continue
                        st['pairs'] += 1
                        d = dist(e, f)
                        if any(dist(g, f) < d for g in nbr[e]) or any(dist(e, g) < d for g in nbr[f]):
                            continue
                        st['STUCK'] += 1
                        if st['STUCK'] <= 10:
                            print('STUCK m', m, 'p', p, 'n', n, 'N', N, {V[k]: c for k, c in enumerate(e) if c},
                                  {V[k]: c for k, c in enumerate(f) if c}, 'caps>1', {s: cap[s] for s in V if cap[s] > 1}, flush=True)
    print('m', m, dict(st), flush=True)
