# Faster rule-based search: order p-free r by (largest prime factor desc, r asc) so that the balance of each prime
# is checked as soon as its group is complete; local rules checked whenever all members of a triple r*r2 = s are
# assigned.  Reports configurations with balance, t >= 2 satisfying (Prod), (Quot), (Quot'), (Prod-).
import sys
from collections import Counter, defaultdict
from sympy import factorint

n = int(sys.argv[1]); p = int(sys.argv[2]); LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 10**8
L = 0
while p ** (L + 1) <= n: L += 1
T0 = L * (L + 1) // 2
R = [r for r in range(2, n + 1) if r % p]
Rset = set(R)
ell = {}
for r in R:
    k = 0; v = r
    while v <= n: k += 1; v *= p
    ell[r] = k
fac = {r: factorint(r) for r in R}
order = sorted(R, key=lambda r: (-max(fac[r]), r))
pos = {r: i for i, r in enumerate(order)}
# triples (r, r2, s) with r*r2 = s, r <= r2
triples = []
for s in R:
    for r in R:
        if r * r > s: break
        if s % r == 0 and (s // r) in Rset:
            triples.append((r, s // r, s))
by_elem = defaultdict(list)
for tr in triples:
    last = max(tr, key=lambda x: pos[x])
    by_elem[last].append(tr)
# group ends for balance
group_end = {}
for i, r in enumerate(order):
    q = max(fac[r])
    group_end[q] = i
end_at = defaultdict(list)
for q, i in group_end.items(): end_at[i].append(q)

A = {}; Bt = {}
st = Counter(); found = []

def m(r): return ell[r] - Bt[r]

def check_triple(r, r2, s):
    a, b = A[s], Bt[s]
    ar, ar2 = A[r], A[r2]
    if r != r2:
        if ar >= 1 and ar2 >= 1 and a < min(ell[s], ar + ar2 - 1): return False
    else:
        if ar >= 2 and a < min(ell[s], 2 * ar - 2): return False
    for (x, y) in ((r, r2), (r2, r)) if r != r2 else ((r, r),):
        # Quot: x in R+, s in R-, beta_y >= 1 : beta_s >= alpha_x + beta_y - 1
        if A[x] >= 1 and m(s) >= 1 and Bt[y] >= 1 and b < A[x] + Bt[y] - 1: return False
        # Quot': s in R+, x in R-, alpha_y < ell_y : alpha_s <= beta_x + alpha_y
        if a >= 1 and m(x) >= 1 and A[y] < ell[y] and a > Bt[x] + A[y]: return False
    # Prod-: r, r2 in R-, beta_s >= 1: beta_s <= beta_r + beta_r2 (r == r2: 2 beta + 1)
    if m(r) >= 1 and m(r2) >= 1 and b >= 1:
        lim = Bt[r] + Bt[r2] if r != r2 else 2 * Bt[r] + 1
        if b > lim: return False
    return True

def tval():
    t = -T0
    for r in R:
        a, b = A[r], Bt[r]
        t += a * (a - 1) // 2
        t -= sum(range(b, ell[r]))
    return t

def dfs(i):
    if len(found) >= 5 or st['nodes'] > LIMIT: return
    st['nodes'] += 1
    if i == len(order):
        st['balanced'] += 1
        t = tval()
        st['maxt'] = max(st['maxt'], t) if 'maxt' in st else t
        if t >= 2:
            st['T>=2'] += 1
            found.append({r: (A[r], Bt[r]) for r in R if (A[r], Bt[r]) != (0, ell[r])})
        return
    s = order[i]
    for a in range(ell[s] + 1):
        for b in range(a, ell[s] + 1):
            A[s] = a; Bt[s] = b
            good = all(check_triple(*tr) for tr in by_elem[s])
            if good:
                for q in end_at[i]:
                    tot = sum(fac[r][q] * (A[r] - m(r)) for r in order[:i + 1] if r % q == 0)
                    if tot != 0: good = False; break
            if good: dfs(i + 1)
            del A[s]; del Bt[s]
dfs(0)
print('n', n, 'p', p, 'L', L, dict(st), flush=True)
for f in found: print('  FOUND', f)
