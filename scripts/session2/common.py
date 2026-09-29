# Common helpers for exploring Lemma L / bridge lemma
from collections import defaultdict
from sympy import divisors, factorint, isprime, primerange

def caps_real(n, p, x):
    """W = p-free s in [2, x-1], caps L_s = #{i>=0 : s p^i <= n}."""
    W = [s for s in range(2, x) if s % p]
    cap = {}
    for s in W:
        k = 0; v = s
        while v <= n:
            k += 1; v *= p
        cap[s] = k
    return W, cap

def all_reps(W, cap, limit=None):
    """dict N -> list of reps (tuple of counts aligned with W)."""
    reps = {1: [tuple([0]*len(W))]}
    for i, s in enumerate(W):
        nr = defaultdict(list)
        for R, lst in reps.items():
            v = R
            for j in range(cap[s] + 1):
                if limit is not None and v > limit:
                    break
                for e in lst:
                    if j:
                        ee = list(e); ee[i] = j; ee = tuple(ee)
                    else:
                        ee = e
                    nr[v].append(ee)
                v *= s
        reps = nr
    return reps

def dist(e, f):
    return sum(abs(a - b) for a, b in zip(e, f))
