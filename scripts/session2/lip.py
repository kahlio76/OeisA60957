# (Lip) test for x = a*b (a<b primes) in the framework-B world V = p-free s < x with caps from n (profile scan).
# For each {a,b}-free part N_O: F = {(e_a, e_b) : N_O a^e_a b^e_b in S(V)}.
# Row j: [A(j), B(j)]. Check: rows are intervals; nonempty rows form an interval;
# (LipA) A(j+1) <= A(j) + 1 ; (LipB) B(j+1) <= B(j) + 1 ; also the Lemma-L diagonal property directly.
import sys
from collections import Counter, defaultdict
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
only_nontriv = len(sys.argv) > 3 and sys.argv[3] == 'nontriv'
st = Counter()
for x in range(6, XMAX + 1):
    F_ = factorint(x)
    if not (len(F_) == 2 and all(v == 1 for v in F_.values())): continue
    a, b = sorted(F_)
    for p in primerange(2, NMAX + 1):
        if x % p == 0: continue
        W = [s for s in range(2, x) if s % p]
        if only_nontriv and not any(s < a for s in W): continue
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 3000000: st['skip'] += 1; continue
            st['profiles'] += 1
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
                if js != list(range(js[0], js[-1] + 1)):
                    st['ROWS_NOT_INTERVAL_OF_J'] += 1
                A = {}; B = {}
                for j in js:
                    r = sorted(rows[j])
                    if r != list(range(r[0], r[-1] + 1)): st['ROW_HOLE'] += 1
                    A[j], B[j] = r[0], r[-1]
                for j in js[:-1]:
                    if j + 1 not in A: continue
                    st['steps'] += 1
                    if A[j + 1] > A[j] + 1:
                        st['LipA_FAIL'] += 1
                        if st['LipA_FAIL'] <= 5: print('LipA_FAIL x', x, 'p', p, 'n', n, 'NO', NO, 'j', j, A[j], A[j + 1], flush=True)
                    if B[j + 1] > B[j] + 1:
                        st['LipB_FAIL'] += 1
                        if st['LipB_FAIL'] <= 5: print('LipB_FAIL x', x, 'p', p, 'n', n, 'NO', NO, 'j', j, B[j], B[j + 1], flush=True)
                # direct diagonal check
                for (ea, eb) in pts:
                    for t in range(2, 6):
                        if (ea + t, eb + t) in pts and (ea + 1, eb + 1) not in pts:
                            st['LFAIL'] += 1
    print('x', x, dict(st), flush=True)
