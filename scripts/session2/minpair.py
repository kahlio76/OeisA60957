# Minimal-distance pairs for the bridge (framework B, real caps, profile scan).
# For each bridge instance (N, N*x in S), compute d* = min |X - Q|_1 over Q in R(N), X in R(Nx),
# and check whether ALL / SOME minimal pairs are M-adjacent. Also record shapes of minimal pairs.
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of, madj

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
PAIRMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 200000
st = Counter(); shapes = Counter(); ex = {}
for x in range(4, XMAX + 1):
    if isprime(x):
        continue
    for p in primerange(2, NMAX + 1):
        if x % p == 0:
            continue
        W = [s for s in range(2, x) if s % p]
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen:
                continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 1500000:
                st['skip_big'] += 1; continue
            for N in S[0]:
                if N * x not in S[0]:
                    continue
                RN = all_reps_of(N, W, cap, S); RX = all_reps_of(N * x, W, cap, S)
                if len(RN) * len(RX) > PAIRMAX:
                    st['skip_pairs'] += 1; continue
                st['inst'] += 1
                best = None; pairs = []
                for Q in RN:
                    for X in RX:
                        d = sum(abs(a - b) for a, b in zip(Q, X))
                        if best is None or d < best:
                            best = d; pairs = [(Q, X)]
                        elif d == best:
                            pairs.append((Q, X))
                flags = [madj(Q, X) for Q, X in pairs]
                if all(flags): st['all_min_madj'] += 1
                elif any(flags): st['some_min_madj'] += 1
                else:
                    st['NO_min_madj'] += 1
                    Q, X = pairs[0]
                    print('NOMIN x', x, 'p', p, 'n', n, 'N', N, 'd', best, 'Q', {W[i]: c for i, c in enumerate(Q) if c},
                          'D+', {W[i]: X[i] - Q[i] for i in range(len(W)) if X[i] > Q[i]},
                          'D-', {W[i]: Q[i] - X[i] for i in range(len(W)) if Q[i] > X[i]}, flush=True)
                for Q, X in pairs[:1]:
                    sh = (sum(max(0, a - b) for a, b in zip(Q, X)), sum(max(0, b - a) for a, b in zip(Q, X)))
                    shapes[sh] += 1
                    if len(ex.setdefault(sh, [])) < 2:
                        ex[sh].append((x, p, n, N, {W[i]: X[i] - Q[i] for i in range(len(W)) if X[i] != Q[i]}))
    print('x', x, dict(st), dict(sorted(shapes.items())), flush=True)
for sh, L in sorted(ex.items()):
    print('shape (|D-|,|D+|)', sh, L)
