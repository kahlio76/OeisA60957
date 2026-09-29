# For x = a*b: (Lip-A) A(j+1) <= A(j)+1. Find rows j where EVERY min-a rep Y of row j is b-saturated
# (no rep of row j+1 with the same a-content obtainable by a single b-insertion).  For those, record the minimal
# distance from some min-a rep Y (row j) to a rep Y' of row j+1 with a-content <= A(j)+1.
import sys
from collections import Counter, defaultdict
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
REPMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
st = Counter(); dist_needed = Counter(); ex = []
def dist(u, v): return sum(abs(i - j) for i, j in zip(u, v))
for x in range(6, XMAX + 1):
    F_ = factorint(x)
    if not (len(F_) == 2 and all(v == 1 for v in F_.values())): continue
    a, b = sorted(F_)
    for p in primerange(2, NMAX + 1):
        if x % p == 0: continue
        W = [s for s in range(2, x) if s % p]
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 1500000: continue
            groups = defaultdict(set)
            for N in S[0]:
                u = N; ea = eb = 0
                while u % a == 0: u //= a; ea += 1
                while u % b == 0: u //= b; eb += 1
                groups[u].add((ea, eb))
            for NO, pts in groups.items():
                rows = defaultdict(list)
                for ea, eb in pts: rows[eb].append(ea)
                for j in sorted(rows):
                    if j + 1 not in rows: continue
                    Aj = min(rows[j]); Aj1 = min(rows[j + 1])
                    if Aj1 <= Aj:
                        # check whether it is 'trivial' (some min rep has a b-insertion single move)
                        pass
                    Y0 = all_reps_of(NO * a**Aj * b**j, W, cap, S)
                    if len(Y0) > REPMAX: st['skip'] += 1; continue
                    tgt = []
                    for e in range(Aj1, Aj + 2):
                        if e in rows[j + 1]:
                            R = all_reps_of(NO * a**e * b**(j + 1), W, cap, S)
                            if len(R) > REPMAX: tgt = None; break
                            tgt += R
                    if tgt is None: st['skip'] += 1; continue
                    st['steps'] += 1
                    if not tgt:
                        st['LipA_FAIL'] += 1; continue
                    d = min(dist(Y, Z) for Y in Y0 for Z in tgt)
                    dist_needed[d] += 1
                    if d >= 3 and len(ex) < 16:
                        Y, Z = min(((Y, Z) for Y in Y0 for Z in tgt), key=lambda yz: dist(*yz))
                        ex.append((x, p, n, NO, j, Aj, {W[i]: Y[i] for i in range(len(W)) if Y[i]}, {W[i]: Z[i] - Y[i] for i in range(len(W)) if Z[i] != Y[i]}))
    print('x', x, dict(st), 'dist needed', dict(sorted(dist_needed.items())), flush=True)
for e in ex: print('EX', e)
