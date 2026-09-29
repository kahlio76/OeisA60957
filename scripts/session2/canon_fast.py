# Fast test: canonical lex-greedy rep Q (max count of smallest element first) admits simple insertion.
# Usage: canon_fast.py N0 N1 [mode]  mode in {lexsmall, lexlarge}
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from common import caps_real
from simple_ins_lib import simple_insert

def suffix_sets(W, cap, bound=None):
    """S[i] = set of products over W[i:], with caps."""
    k = len(W)
    S = [None] * (k + 1)
    S[k] = {1}
    for i in range(k - 1, -1, -1):
        s = W[i]; cur = set(S[i + 1]); base = S[i + 1]
        v = 1
        for j in range(1, cap[s] + 1):
            v *= s
            cur.update(y * v for y in base)
        S[i] = cur
    return S

def greedy_rep(N, W, cap, S, order):
    e = [0] * len(W)
    rem = N
    for i in order:
        s = W[i]
        # choose max (or min) count
        best = None
        for j in range(cap[s], -1, -1):
            if rem % (s ** j) == 0 and (rem // s ** j) in S_after[i]:
                best = j; break
        if best is None:
            return None
        e[i] = best; rem //= s ** best
    return tuple(e) if rem == 1 else None

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
st = Counter()
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        for x in range(4, n + 1):
            if x % p == 0 or isprime(x):
                continue
            W, cap = caps_real(n, p, x)
            idx = {w: i for i, w in enumerate(W)}
            S = suffix_sets(W, cap)
            S_after = [S[i + 1] for i in range(len(W))]
            full = S[0]
            for N in full:
                if not any(N * x**t in full for t in range(2, 8)):
                    continue
                st['inst'] += 1
                if N * x not in full:
                    st['LFAIL'] += 1; print('LFAIL', n, p, x, N, flush=True); continue
                Q = greedy_rep(N, W, cap, S, range(len(W)))
                if not simple_insert(Q, W, idx, cap, x):
                    st['FAIL'] += 1
                    if st['FAIL'] <= 20:
                        print('FAIL', n, p, x, factorint(x), N, {W[i]: c for i, c in enumerate(Q) if c}, flush=True)
    print('n', n, dict(st), flush=True)
