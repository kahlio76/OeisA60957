# Two-step bridge test for x with >= 2 prime factors (class-C / framework B setting, profile scan).
# For bridge instances (N, Nx in S): pick a prime factor q of x, x = q*y.
#  (i)  is N*q in S  or  N*y in S  for some factorization x = q*y (q prime)?
#  (ii) exists Y in R(N*q) with a single q-down-move to R(N) and an M-adjacent 'y-insertion' to R(Nx)
#       where we require X - Y to be a single move (entries in {-1,0,1}, at most one +1 and one -1 ... or
#       for y composite: any M-adjacent X with X - Q M-adjacent overall).
# We test the precise route used in the proof sketch: exists Y in R(Nq) and Q in R(N), X in R(Nx) with
# Y - Q a single move (<=1 entry +1, <=1 entry -1, rest 0) and X - Y a single move.
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of

def single(e, f):
    """f - e has at most one +1 and at most one -1 and nothing else."""
    pos = neg = 0
    for a, b in zip(e, f):
        d = b - a
        if d == 1: pos += 1
        elif d == -1: neg += 1
        elif d != 0: return False
    return pos <= 1 and neg <= 1

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
PAIRMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 200000
st = Counter()
for x in range(4, XMAX + 1):
    if isprime(x): continue
    F = factorint(x)
    if len(F) < 2: continue
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
            if len(S[0]) > 800000: continue
            for N in S[0]:
                if N * x not in S[0]: continue
                st['inst'] += 1
                mids = [q for q in F if N * q in S[0]] + [x // q for q in F if N * (x // q) in S[0] and x // q in cap]
                if not mids:
                    st['NO_intermediate'] += 1
                    if st['NO_intermediate'] <= 6: print('NOMID x', x, 'p', p, 'n', n, 'N', N, flush=True)
                    continue
                ok = False
                RN = all_reps_of(N, W, cap, S); RX = all_reps_of(N * x, W, cap, S)
                for q in set(mids):
                    RY = all_reps_of(N * q, W, cap, S)
                    if len(RY) * (len(RN) + len(RX)) > PAIRMAX: continue
                    for Y in RY:
                        if any(single(Q, Y) for Q in RN) and any(single(Y, X) for X in RX):
                            ok = True; break
                    if ok: break
                st['twostep_ok' if ok else 'twostep_FAIL'] += 1
                if not ok and st['twostep_FAIL'] <= 6:
                    print('TWOSTEP_FAIL x', x, 'p', p, 'n', n, 'N', N, 'mids', mids, flush=True)
    print('x', x, dict(st), flush=True)
