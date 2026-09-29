# For bridge (N, Nx) and Lemma-L (N, Nx^t) instances: is there a pair (Q in R(N), X in R(N x^j)) with the SAME
# P_x-free core multiset (multiset of the parts of blocks coprime to x, excluding 1)?
# If yes for bridges, also check whether such a same-core pair can be chosen M-adjacent.
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of, madj

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
PAIRMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
st = Counter()

def core(e, W, primes):
    c = Counter()
    for i, k in enumerate(e):
        if k:
            u = W[i]
            for q in primes:
                while u % q == 0: u //= q
            if u > 1: c[u] += k
    return tuple(sorted(c.items()))

for x in range(4, XMAX + 1):
    if isprime(x):
        continue
    P = list(factorint(x))
    for p in primerange(2, NMAX + 1):
        if x % p == 0:
            continue
        W = [s for s in range(2, x) if s % p]
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen: continue
            seen.add(key)
            S = suffix_sets(W, cap)
            if len(S[0]) > 800000: continue
            for N in S[0]:
                if N * x not in S[0]:
                    continue
                RN = all_reps_of(N, W, cap, S); RX = all_reps_of(N * x, W, cap, S)
                if len(RN) * len(RX) > PAIRMAX: continue
                st['B_inst'] += 1
                cN = {}
                for Q in RN: cN.setdefault(core(Q, W, P), []).append(Q)
                common = [(Q, X) for X in RX for Q in cN.get(core(X, W, P), [])]
                if not common:
                    st['B_NO_samecore'] += 1
                    if st['B_NO_samecore'] <= 8:
                        print('NO_SAMECORE x', x, factorint(x), 'p', p, 'n', n, 'N', N, flush=True)
                    continue
                if any(madj(Q, X) for Q, X in common): st['B_samecore_madj'] += 1
                else:
                    st['B_samecore_but_not_madj'] += 1
                    if st['B_samecore_but_not_madj'] <= 5:
                        print('SAMECORE_NOT_MADJ x', x, 'p', p, 'n', n, 'N', N, flush=True)
    print('x', x, dict(st), flush=True)
