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

XMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
PMAX = int(sys.argv[3]) if len(sys.argv) > 3 else NMAX
SMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 3_000_000   # skip profiles with |S| too big

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

st = Counter()
for x in range(4, XMAX + 1):
    if isprime(x):
        continue
    for p in primerange(2, PMAX + 1):
        if x % p == 0:
            continue
        W = [s for s in range(2, x) if s % p]
        th = sorted(set(s * p**k for s in W for k in range(0, 40) if x <= s * p**k <= NMAX) | {x})
        seen = set()
        for n in th:
            cap = caps_for(W, p, n)
            key = tuple(cap[s] for s in W)
            if key in seen:
                continue
            seen.add(key)
            # estimate size
            est = 1
            for s in W: est *= (cap[s] + 1)
            S = suffix_sets(W, cap)
            full = S[0]
            if len(full) > SMAX:
                st['skipped_big'] += 1; continue
            idx = {w: i for i, w in enumerate(W)}
            st['profiles'] += 1
            for N in full:
                if N % x == 0 and (N // x) in full:
                    pass
                ts = [t for t in range(0, 12) if N * x**t in full]
                if ts and ts != list(range(len(ts))):
                    st['LFAIL'] += 1; print('LFAIL', x, p, n, N, ts, flush=True)
                if any(t >= 2 for t in ts):
                    st['GL'] += 1
                    Q = greedy_rep(N, W, cap, S)
                    if not simple_insert(Q, W, idx, cap, x):
                        st['GL_FAIL'] += 1
                        if st['GL_FAIL'] <= 25:
                            print('GL_FAIL x', x, factorint(x), 'p', p, 'n', n, 'N', N, 'Q', {W[i]: c for i, c in enumerate(Q) if c}, 'caps', {s: cap[s] for s in W if cap[s] > 1}, flush=True)
                if 1 in ts:
                    st['GQB'] += 1
                    Q = greedy_rep(N, W, cap, S)
                    if not exists_madj(Q, N * x, W, cap, S):
                        st['GQB_FAIL'] += 1
                        # check bridge lemma itself
                        ok = False
                        XS = all_reps_of(N * x, W, cap, S)
                        for Qp in all_reps_of(N, W, cap, S):
                            if any(madj(Qp, X) for X in XS):
                                ok = True; break
                        if not ok:
                            st['BRFAIL'] += 1
                            print('BRFAIL x', x, 'p', p, 'n', n, 'N', N, flush=True)
                        if st['GQB_FAIL'] <= 25:
                            print('GQB_FAIL x', x, factorint(x), 'p', p, 'n', n, 'N', N, 'Q', {W[i]: c for i, c in enumerate(Q) if c}, 'bridge_exists', ok, flush=True)
    print('x', x, dict(st), flush=True)
