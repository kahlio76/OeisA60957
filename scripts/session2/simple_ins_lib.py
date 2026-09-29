# For Lemma L instances (real setting), test "simple insertion":
# x = d1*d2*...*dk (k>=2 factors, each >=2); attach each d_i to a host u_i in supp(Q) U {1}
# (distinct copies), i.e. Q - {u_i} + {u_i d_i}, respecting caps.
# Report: per instance N, whether SOME rep Q admits simple insertion, and whether ALL do.
import sys, itertools
from collections import Counter
from sympy import isprime, primerange, factorint
from common import caps_real, all_reps

def factorizations(x, mn=2):
    """multiplicative partitions of x into factors >= mn (non-decreasing)."""
    res = []
    for d in range(mn, int(x**0.5) + 1):
        if x % d == 0:
            for rest in factorizations(x // d, d):
                res.append([d] + rest)
    res.append([x])
    return res

def simple_insert(Q, W, idx, cap, x):
    # Q: tuple of counts aligned with W
    for fac in factorizations(x):
        if len(fac) < 2:
            continue
        # choose hosts for each factor: host 1 or element of supp Q
        hosts = [1] + [W[i] for i, c in enumerate(Q) if c]
        for hs in itertools.product(hosts, repeat=len(fac)):
            e = dict((W[i], c) for i, c in enumerate(Q) if c)
            ok = True
            for d, h in zip(fac, hs):
                v = d * h
                if v not in idx:
                    ok = False; break
                if h != 1:
                    if e.get(h, 0) < 1:
                        ok = False; break
                    e[h] -= 1
                e[v] = e.get(v, 0) + 1
                if e[v] > cap[v]:
                    ok = False; break
            if ok:
                return True
    return False

