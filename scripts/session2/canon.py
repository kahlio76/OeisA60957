# Test canonical choices of Q for simple insertion (Lemma L, real setting).
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from common import caps_real, all_reps
from simple_ins_lib import simple_insert

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
rules = {
    # most blocks; tie-break lex-max count vector (prefer small elements)
    'finest_lex': lambda W, QL: max(QL, key=lambda Q: (sum(Q), Q)),
    # lex-max count vector indexed by increasing w: as many 2's as possible, then 3's ...
    'lexsmall': lambda W, QL: max(QL),
    # most blocks, tie-break lex-min
    'finest_lexmin': lambda W, QL: max(QL, key=lambda Q: (sum(Q), tuple(-c for c in Q))),
    # min sum of squares of log(block) ~ prefer balanced small blocks
    'minlog2': lambda W, QL: min(QL, key=lambda Q: sum(c * (__import__('math').log(W[i]))**2 for i, c in enumerate(Q))),
}
st = Counter()
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        for x in range(4, n + 1):
            if x % p == 0 or isprime(x):
                continue
            W, cap = caps_real(n, p, x)
            idx = {w: i for i, w in enumerate(W)}
            reps = all_reps(W, cap)
            for N, QL in reps.items():
                if not any(N * x**t in reps for t in range(2, 8)):
                    continue
                st['inst'] += 1
                for name, rule in rules.items():
                    Q = rule(W, QL)
                    if not simple_insert(Q, W, idx, cap, x):
                        st[name + '_FAIL'] += 1
                        if st[name + '_FAIL'] <= 3:
                            print(name, 'FAIL', n, p, x, N, {W[i]: c for i, c in enumerate(Q) if c}, flush=True)
    print('n', n, dict(st), flush=True)
