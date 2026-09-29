# For every non-M-adjacent ratio-1 relation D over V = V(X,Pi) (product <= PMAX), find the certificate
# (proper conformal part with ratio 1 or ratio z^{+-1}, z in V\supp D) of minimum size |A|+|B|, and
# record the distribution of (|A|,|B|, kind) of the best certificate.  Also record whether a certificate
# involving at least one copy of a doubled element exists with |A|+|B| <= 3.
import sys, itertools
from math import prod
from collections import Counter
X = int(sys.argv[1]); PMAX = int(sys.argv[2])
Pi = tuple(int(t) for t in sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] != '-' else ()
V = [s for s in range(2, X) if all(s % q for q in Pi)]
Vset = set(V)
memo = {}
def facts(P, minpart):
    key = (P, minpart)
    if key in memo: return memo[key]
    out = []
    if P == 1: out = [()]
    else:
        for s in V:
            if s < minpart: continue
            if s > P: break
            if P % s == 0:
                for rest in facts(P // s, s): out.append((s,) + rest)
    memo[key] = out
    return out
def madj_ms(Dp, Dm):
    cp = Counter(Dp); cm = Counter(Dm)
    return sum(1 for v in cp.values() if v >= 2) <= 1 and sum(1 for v in cm.values() if v >= 2) <= 1
def subms(ms):
    c = Counter(ms); keys = sorted(c)
    for combo in itertools.product(*[range(c[k] + 1) for k in keys]):
        yield tuple(k for k, m in zip(keys, combo) for _ in range(m)), prod(k ** m for k, m in zip(keys, combo))
cands = {1}
for s in V:
    new = set()
    for v in cands:
        w = v * s
        while w <= PMAX: new.add(w); w *= s
    cands |= new
shapes = Counter(); st = Counter(); ex = {}
for P in sorted(cands):
    if P == 1: continue
    F = facts(P, 2)
    for i in range(len(F)):
        for j in range(len(F)):
            if i == j: continue
            Dp, Dm = F[i], F[j]
            if Dp > Dm or set(Dp) & set(Dm) or madj_ms(Dp, Dm): continue
            # orient so that D+ is a side with two doubled elements (if both sides, keep as is)
            cp = Counter(Dp)
            if sum(1 for v in cp.values() if v >= 2) < 2: Dp, Dm = Dm, Dp
            st['nonmadj'] += 1
            supp = set(Dp) | set(Dm); full = (len(Dp), len(Dm))
            best = None
            for A, pa in subms(Dp):
                for B, pb in subms(Dm):
                    sz = len(A) + len(B)
                    if sz == 0 or (len(A), len(B)) == full: continue
                    if best is not None and sz >= best[0]: continue
                    kind = None
                    if pa == pb: kind = 'one'
                    elif pa % pb == 0 and pa // pb in Vset and pa // pb not in supp: kind = 'z'
                    elif pb % pa == 0 and pb // pa in Vset and pb // pa not in supp: kind = '1/z'
                    if kind: best = (sz, len(A), len(B), kind, A, B)
            if best is None:
                st['NONE'] += 1; print('NONE', Dp, Dm, flush=True); continue
            shapes[best[1:4]] += 1
            if best[0] >= 4 and len(ex) < 12: ex[(Dp, Dm)] = best
print('X', X, 'Pi', Pi, dict(st))
for k, v in sorted(shapes.items(), key=lambda t: -t[1]): print('  shape', k, v)
for k, v in ex.items(): print('EX', k, v)
