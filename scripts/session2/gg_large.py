# (GG) and (GL) for greedy-LARGE (lex-max w.r.t. counts indexed by DECREASING element), real setting (framework B).
import sys
from collections import Counter
from sympy import isprime, primerange
from common import caps_real
from sigreedy_lib import suffix_sets, greedy_rep
from simple_ins_lib import simple_insert
from lexascent_lib import madj

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
st = Counter()
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        for x in range(4, n + 1):
            if x % p == 0 or isprime(x):
                continue
            W, cap = caps_real(n, p, x)
            Wd = W[::-1]
            idx = {w: i for i, w in enumerate(Wd)}
            S = suffix_sets(Wd, cap)
            full = S[0]
            for N in full:
                if N * x in full:
                    st['GG'] += 1
                    Q = greedy_rep(N, Wd, cap, S); G = greedy_rep(N * x, Wd, cap, S)
                    if not madj(Q, G):
                        st['GG_FAIL'] += 1
                        if st['GG_FAIL'] <= 6:
                            print('GG_FAIL', n, p, x, N, {Wd[i]: c for i, c in enumerate(Q) if c}, {Wd[i]: c for i, c in enumerate(G) if c}, flush=True)
                if any(N * x**t in full for t in range(2, 6)):
                    st['GL'] += 1
                    Q = greedy_rep(N, Wd, cap, S)
                    if not simple_insert(Q, Wd, idx, cap, x):
                        st['GL_FAIL'] += 1
                        if st['GL_FAIL'] <= 6:
                            print('GL_FAIL', n, p, x, N, {Wd[i]: c for i, c in enumerate(Q) if c}, flush=True)
    print('n', n, dict(st), flush=True)
