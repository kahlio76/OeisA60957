# (Lip) in GENERAL class-C worlds: V = p-free s in [2, X-1] (Pi = {p}), caps from n >= X (all profiles),
# for every pair of primes a != b (both != p, both < X): rows indexed by e_b, check A(j+1)<=A(j)+1, B(j+1)<=B(j)+1,
# rows are intervals, nonempty rows consecutive.
import sys
from collections import Counter, defaultdict
from sympy import isprime, primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
st = Counter()
for X in range(5, XMAX + 1):
    for p in primerange(2, NMAX + 1):
        W = [s for s in range(2, X) if s % p]
        primes = [q for q in primerange(2, X) if q != p]
        if len(primes) < 2: continue
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if X <= s * p**k <= NMAX) | {X})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 1500000: st['skip'] += 1; continue
            st['worlds'] += 1
            for a in primes:
                for b in primes:
                    if a == b: continue
                    groups = defaultdict(set)
                    for N in S[0]:
                        u = N; ea = eb = 0
                        while u % a == 0: u //= a; ea += 1
                        while u % b == 0: u //= b; eb += 1
                        groups[u].add((ea, eb))
                    for NO, pts in groups.items():
                        rows = defaultdict(list)
                        for ea, eb in pts: rows[eb].append(ea)
                        js = sorted(rows)
                        if js != list(range(js[0], js[-1] + 1)): st['ROWJ_GAP'] += 1
                        A = {}; B = {}
                        for j in js:
                            r = sorted(rows[j])
                            if r != list(range(r[0], r[-1] + 1)): st['ROW_HOLE'] += 1
                            A[j], B[j] = r[0], r[-1]
                        for j in js:
                            if j + 1 in A:
                                st['steps'] += 1
                                if A[j + 1] > A[j] + 1:
                                    st['LipA_FAIL'] += 1
                                    if st['LipA_FAIL'] <= 5: print('LipA_FAIL X', X, 'p', p, 'n', n, 'a', a, 'b', b, 'NO', NO, 'j', j, A[j], A[j + 1], flush=True)
                                if B[j + 1] > B[j] + 1:
                                    st['LipB_FAIL'] += 1
                                    if st['LipB_FAIL'] <= 5: print('LipB_FAIL X', X, 'p', p, 'n', n, 'a', a, 'b', b, 'NO', NO, 'j', j, B[j], B[j + 1], flush=True)
    print('X', X, dict(st), flush=True)
