# For PRIMITIVE (no proper ratio-1 part) non-M-adjacent ratio-1 relations D over V(X,Pi), find the minimum size
# of a single-catalyst part and its type.  Question: is there always a catalyst part of size <= 3?
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
def ndoubled(ms):
    return sum(1 for v in Counter(ms).values() if v >= 2)
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
st = Counter(); shapes = Counter(); ex = []
for P in sorted(cands):
    if P == 1: continue
    F = facts(P, 2)
    for i in range(len(F)):
        for j in range(i + 1, len(F)):
            Dp, Dm = F[i], F[j]
            if set(Dp) & set(Dm): continue
            if ndoubled(Dp) <= 1 and ndoubled(Dm) <= 1: continue
            if ndoubled(Dp) < 2: Dp, Dm = Dm, Dp
            supp = set(Dp) | set(Dm); full = (len(Dp), len(Dm))
            SP = list(subms(Dp)); SM = list(subms(Dm))
            prim = True; best = None
            for A, pa in SP:
                for B, pb in SM:
                    la, lb = len(A), len(B)
                    if (la, lb) == (0, 0) or (la, lb) == full: continue
                    if pa == pb: prim = False; break
                    kind = None
                    if pa % pb == 0 and pa // pb in Vset and pa // pb not in supp: kind = 'z'
                    elif pb % pa == 0 and pb // pa in Vset and pb // pa not in supp: kind = '1/z'
                    if kind and (best is None or la + lb < best[0]): best = (la + lb, la, lb, kind, A, B)
                if not prim: break
            if not prim: continue
            st['prim_nonmadj'] += 1
            if best is None:
                st['NONE'] += 1; print('NONE', Dp, Dm, flush=True); continue
            shapes[best[1:4]] += 1
            if best[0] >= 3 and len(ex) < 60: ex.append((Dp, Dm, best))
print('X', X, 'Pi', Pi, 'PMAX', PMAX, dict(st))
for k, v in sorted(shapes.items(), key=lambda t: -t[1]): print('  shape', k, v)
for e in ex: print('EX', e)
