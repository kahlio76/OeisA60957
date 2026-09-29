# MC with ARBITRARY (random, non-monotone) caps in class-C sets V = V(X, Pi) = {s in [2,X): gcd(s,Pi)=1}.
# Also tests (L*)/(B) for the next element x with these caps.  If MC holds for arbitrary caps, a caps-free
# ("catalyst") proof is plausible.
import sys, random
from math import gcd
from collections import Counter
from sympy import primerange, isprime
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of, madj

XMAX = int(sys.argv[1]); TRIALS = int(sys.argv[2]); CMAX = int(sys.argv[3])
REPCAP = int(sys.argv[4]) if len(sys.argv) > 4 else 300
SMAX = int(sys.argv[5]) if len(sys.argv) > 5 else 200000
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 1
random.seed(seed)
st = Counter()
PIS = [(), (2,), (3,), (5,), (2, 3), (7,)]

def components(R):
    par = list(range(len(R)))
    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    for i in range(len(R)):
        for j in range(i + 1, len(R)):
            if madj(R[i], R[j]):
                a, b = f(i), f(j)
                if a != b: par[a] = b
    return len({f(i) for i in range(len(R))})

for X in range(6, XMAX + 1):
    for Pi in PIS:
        V = [s for s in range(2, X) if all(s % q for q in Pi)]
        if len(V) < 3: continue
        for trial in range(TRIALS):
            cap = {s: random.randint(1, CMAX) for s in V}
            S = suffix_sets(V, cap)
            if len(S[0]) > SMAX: st['skip'] += 1; continue
            st['worlds'] += 1
            for N in S[0]:
                R = all_reps_of(N, V, cap, S)
                if len(R) < 2 or len(R) > REPCAP: continue
                st['prods'] += 1
                k = components(R)
                if k > 1:
                    st['MC_FAIL'] += 1
                    if st['MC_FAIL'] <= 10:
                        print('MC_FAIL X', X, 'Pi', Pi, 'caps', {s: cap[s] for s in V}, 'N', N, 'reps',
                              [{V[i]: c for i, c in enumerate(r) if c} for r in R][:8], flush=True)
            # (L*) and (B) for the next element x
            x = X
            while any(x % q == 0 for q in Pi): x += 1
            if isprime(x): continue
            SS = S[0]
            for N in SS:
                if N * x in SS:
                    st['B_inst'] += 1
                else:
                    t = 2; v = N * x * x
                    mx = max(SS)
                    while v <= mx:
                        if v in SS:
                            st['LSTAR_FAIL'] += 1
                            if st['LSTAR_FAIL'] <= 10:
                                print('LSTAR_FAIL X', X, 'Pi', Pi, 'x', x, 'caps', {s: cap[s] for s in V}, 'N', N, 't', t, flush=True)
                            break
                        v *= x; t += 1
    print('X', X, dict(st), flush=True)
