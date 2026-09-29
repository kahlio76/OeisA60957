# Direction-aware Lipschitz property (Lip_v) for two-prime x = a^k b^l in world V = p-free s < x (caps from n).
# F = {(ea, eb)} slice for fixed {a,b}-free part N_O.
# Rows (index eb = j, a-fiber [A(j),B(j)]):  RowLip_v:  A(j+l) <= A(j)+k  and  B(j+l) <= B(j)+k   (rows j, j+l nonempty)
# Cols (index ea = i, b-fiber [C(i),D(i)]):  ColLip_v:  C(i+k) <= C(i)+l  and  D(i+k) <= D(i)+l
# Either one (plus fibers intervals + nonempty rows/cols consecutive) implies (L*) along v=(k,l).
# Also: the slope-1 version in the orientation where the step is along the SMALLER exponent is weaker... we record all.
import sys
from collections import Counter, defaultdict
from sympy import primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
SMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 3000000
st = Counter()
shown = Counter()
for x in range(6, XMAX + 1):
    F_ = factorint(x)
    if len(F_) != 2: continue
    a, b = sorted(F_)
    k, l = F_[a], F_[b]
    for p in primerange(2, NMAX + 1):
        if x % p == 0: continue
        W = [s for s in range(2, x) if s % p]
        th = sorted(set(s * p**e for s in W for e in range(0, 40) if x <= s * p**e <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > SMAX: st['skip'] += 1; continue
            st['profiles'] += 1
            groups = defaultdict(set)
            for N in S[0]:
                u = N; ea = eb = 0
                while u % a == 0: u //= a; ea += 1
                while u % b == 0: u //= b; eb += 1
                groups[u].add((ea, eb))
            for NO, pts in groups.items():
                rows = defaultdict(list); cols = defaultdict(list)
                for ea, eb in pts: rows[eb].append(ea); cols[ea].append(eb)
                A = {j: min(v) for j, v in rows.items()}; B = {j: max(v) for j, v in rows.items()}
                C = {i: min(v) for i, v in cols.items()}; D = {i: max(v) for i, v in cols.items()}
                rowok = colok = True
                for j in A:
                    if j + l in A:
                        st['rsteps'] += 1
                        if A[j + l] > A[j] + k or B[j + l] > B[j] + k:
                            rowok = False; st['RowLipV_FAIL'] += 1
                            if shown['r', x] < 2:
                                shown['r', x] += 1
                                print('RowLipV_FAIL x', x, 'p', p, 'n', n, 'NO', NO, 'j', j, (A[j], B[j]), (A[j + l], B[j + l]), flush=True)
                for i in C:
                    if i + k in C:
                        st['csteps'] += 1
                        if C[i + k] > C[i] + l or D[i + k] > D[i] + l:
                            colok = False; st['ColLipV_FAIL'] += 1
                            if shown['c', x] < 2:
                                shown['c', x] += 1
                                print('ColLipV_FAIL x', x, 'p', p, 'n', n, 'NO', NO, 'i', i, (C[i], D[i]), (C[i + k], D[i + k]), flush=True)
                if not rowok and not colok:
                    st['BOTH_FAIL'] += 1
                    if shown['both', x] < 3:
                        shown['both', x] += 1
                        print('BOTH_FAIL x', x, 'p', p, 'n', n, 'NO', NO, sorted(pts), flush=True)
                for (ea, eb) in pts:
                    for t in range(2, 8):
                        if (ea + k * t, eb + l * t) in pts and (ea + k, eb + l) not in pts:
                            st['LFAIL'] += 1
    print('x', x, (a, k), (b, l), dict(st), flush=True)
