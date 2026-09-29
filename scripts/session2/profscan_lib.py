# Profile scan (framework B, real caps): for each p-free composite x <= XMAX and prime p (p != factors of x),
# iterate over all distinct cap profiles (n ranges over thresholds s*p^k, s<x p-free, n>=x, n<=NMAX).
# Tests:
#   LEMMA L itself (fiber interval along x)
#   GL : N*x^t in S (t>=2) => greedy-small rep of N admits simple insertion
#   GQB: N, N*x in S => exists rep X of N*x M-adjacent (as a bridge) to greedy-small rep Q of N   [DFS search]
#   BR : bridge lemma itself (exists some pair) -- only checked when GQB fails (full search over reps of N)
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from sigreedy_lib import suffix_sets, greedy_rep
from simple_ins_lib import simple_insert





def caps_for(W, p, n):
    cap = {}
    for s in W:
        k = 0; v = s
        while v <= n:
            k += 1; v *= p
        cap[s] = k
    return cap

def exists_madj(Q, target, W, cap, S):
    """DFS: exists rep X of target with X-Q having <=1 coord >=2 and <=1 coord <=-2."""
    m = len(W)
    def rec(i, rem, up, dn):
        if i == m:
            return rem == 1
        if rem not in S[i]:
            return False
        s = W[i]; v = 1
        for j in range(cap[s] + 1):
            if j:
                v *= s
                if rem % v:
                    break
            d = j - Q[i]
            nu = up + (d >= 2); nd = dn + (d <= -2)
            if nu <= 1 and nd <= 1 and rec(i + 1, rem // v, nu, nd):
                return True
        return False
    return rec(0, target, 0, 0)

def all_reps_of(target, W, cap, S):
    m = len(W); out = []
    def rec(i, rem, cur):
        if i == m:
            if rem == 1: out.append(tuple(cur))
            return
        if rem not in S[i]: return
        s = W[i]; v = 1
        for j in range(cap[s] + 1):
            if j:
                v *= s
                if rem % v: break
            cur.append(j); rec(i + 1, rem // v, cur); cur.pop()
    rec(0, target, [])
    return out

def madj(e, f):
    up = dn = 0
    for a, b in zip(e, f):
        d = b - a
        if d >= 2: up += 1
        elif d <= -2: dn += 1
    return up <= 1 and dn <= 1

