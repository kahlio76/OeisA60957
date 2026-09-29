# SI-greedy test: for W = p-free s in [2,x-1] with caps from n (framework B) and x p-free composite:
# if N in S and N*x^t in S for some t>=1, then the lex-greedy (small-first) rep Q of N admits a
# simple insertion of x (each factor d_i of some factorization of x attached to a host in supp(Q) U {1}).
# Usage: sigreedy.py N0 N1 [mode]   mode B (default): caps from n, x<=n.  mode A: framework A, W=p-free<=n-1 caps from n-1, x=n.
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from common import caps_real
from simple_ins_lib import simple_insert

def suffix_sets(W, cap):
    k = len(W); S = [None] * (k + 1); S[k] = {1}
    for i in range(k - 1, -1, -1):
        s = W[i]; base = S[i + 1]; cur = set(base); v = 1
        for j in range(1, cap[s] + 1):
            v *= s; cur.update(y * v for y in base)
        S[i] = cur
    return S

def greedy_rep(N, W, cap, S):
    e = [0] * len(W); rem = N
    for i, s in enumerate(W):
        for j in range(cap[s], -1, -1):
            if rem % (s ** j) == 0 and (rem // s ** j) in S[i + 1]:
                e[i] = j; rem //= s ** j; break
        else:
            return None
    return tuple(e) if rem == 1 else None

def run(n, p, x, W, cap, st):
    idx = {w: i for i, w in enumerate(W)}
    S = suffix_sets(W, cap); full = S[0]
    for N in full:
        ts = [t for t in range(1, 8) if N * x**t in full]
        if not ts:
            continue
        key = 'L' if any(t >= 2 for t in ts) else 'Bonly'
        st[key] += 1
        Q = greedy_rep(N, W, cap, S)
        if not simple_insert(Q, W, idx, cap, x):
            st[key + '_FAIL'] += 1
            if st[key + '_FAIL'] <= 12:
                print('FAIL', key, 'n', n, 'p', p, 'x', x, factorint(x), 'N', N, 'Q', {W[i]: c for i, c in enumerate(Q) if c}, flush=True)

N0, N1 = int(sys.argv[1]), int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else 'B'
st = Counter()
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        if mode == 'B':
            for x in range(4, n + 1):
                if x % p == 0 or isprime(x):
                    continue
                W, cap = caps_real(n, p, x)
                run(n, p, x, W, cap, st)
        else:
            x = n
            if x % p == 0 or isprime(x):
                continue
            W, cap = caps_real(n - 1, p, x)
            run(n, p, x, W, cap, st)
    print('n', n, dict(st), flush=True)
