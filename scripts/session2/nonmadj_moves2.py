# For semiprime bridge instances: take NON-M-adjacent pairs (Q,X) and list which 3-block moves shorten them.
# Classify a move as (side, kind, pattern) where pattern records which of the 3 changes are 'good'.
# Report, for each "non-M-adjacency type", the distribution of available shortening move patterns,
# and look for pairs where only 'exotic' patterns work.
import sys
from collections import Counter
from sympy import isprime, primerange, factorint, divisors
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of, madj

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
PAIRMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
st = Counter(); pat = Counter(); needed = Counter(); ex = {}

def moves(E, W, idx, cap, Dsign, side):
    """all merges/splits of rep E (as dict counts over W); yield (desc, removed, added)."""
    items = [w for w in W if E[idx[w]] > 0]
    out = []
    # merges
    for i, y in enumerate(items):
        for y2 in items[i:]:
            if y2 == y and E[idx[y]] < 2: continue
            m = y * y2
            if m in idx:
                out.append(('merge', (y, y2), (m,)))
    # splits
    for w in items:
        for d in divisors(w):
            if 1 < d and d * d <= w:
                e = w // d
                if d in idx and e in idx:
                    out.append(('split', (w,), (d, e)))
    return out

for x in range(4, XMAX + 1):
    if isprime(x): continue
    F = factorint(x)
    if not (len(F) == 2 and all(v == 1 for v in F.values())): continue
    for p in primerange(2, NMAX + 1):
        if x % p == 0: continue
        W = [s for s in range(2, x) if s % p]; idx = {w: i for i, w in enumerate(W)}
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 500000: continue
            for N in S[0]:
                if N * x not in S[0]: continue
                RN = all_reps_of(N, W, cap, S); RX = all_reps_of(N * x, W, cap, S)
                if len(RN) * len(RX) > PAIRMAX: continue
                for Q in RN:
                    for X in RX:
                        if madj(Q, X): continue
                        st['nonmadj'] += 1
                        D = [xx - qq for xx, qq in zip(X, Q)]
                        def sgn(w): return D[idx[w]]
                        good = []
                        for side, E in (('X', X), ('Q', Q)):
                            for kind, rem, add in moves(E, W, idx, cap, None, side):
                                # validity: counts after
                                cnt = Counter()
                                for r in rem: cnt[r] -= 1
                                for a_ in add: cnt[a_] += 1
                                ok = all(0 <= E[idx[w]] + c <= cap[w] for w, c in cnt.items())
                                if not ok: continue
                                # new D and its l1
                                newD = list(D)
                                for w, c in cnt.items():
                                    newD[idx[w]] += c if side == 'X' else -c
                                if sum(map(abs, newD)) < sum(map(abs, D)):
                                    # describe goodness pattern
                                    g = []
                                    for r in rem: g.append(('rm', 'D+' if sgn(r) > 0 else ('D-' if sgn(r) < 0 else '0')))
                                    for a_ in add: g.append(('add', 'D+' if sgn(a_) > 0 else ('D-' if sgn(a_) < 0 else '0')))
                                    good.append((side, kind, tuple(sorted(g))))
                        if not good:
                            st['NO_3MOVE'] += 1
                            print('NO3', x, p, n, N, flush=True)
                            continue
                        for gm in set(good): pat[gm] += 1
                        # canonical triple-level description (merge in X == split in Q)
                        trip = set()
                        for side, kind, g in good:
                            trip.add(g if side == 'X' else tuple(sorted((('rm' if a_=='add' else 'add'), ('D-' if s=='D+' else ('D+' if s=='D-' else '0'))) for a_, s in g)))
                        needed[len(trip)] += 1
                        if len(trip) == 1 and len(ex) < 25:
                            key2 = (x, tuple(sorted(trip)))
                            if key2 not in ex:
                                ex[key2] = (p, n, N, {W[i]: c for i, c in enumerate(Q) if c}, {W[i]: D[i] for i in range(len(W)) if D[i]}, sorted(set(good))[:2])
    print('x', x, dict(st), flush=True)
print('distinct triple-patterns per pair:', dict(sorted(needed.items())))
for k, v in ex.items(): print('ONLY', k, v)
print('pattern frequencies (a pair may have several):')
for k, v in pat.most_common(40): print('  ', v, k)
