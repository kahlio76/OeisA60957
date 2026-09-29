# For ratio-x relations D (prod D+ = x prod D-) over V = V(X,Pi) (x = next element) with |D-| >= 2, find the
# minimal certificate (proper part E' with ratio in {1, x} u {w, 1/w, x w, x/w : w in V \ supp D}) and record its
# shape (|A|, |B|, kind).  Also: restrict to relations with NO certificate of size <= 2 and show them.
import sys, itertools
from math import prod
from collections import Counter
X = int(sys.argv[1]); PMAX = int(sys.argv[2])
Pi = tuple(int(t) for t in sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] != '-' else ()
V = [s for s in range(2, X) if all(s % q for q in Pi)]
Vset = set(V)
x = X
while any(x % q == 0 for q in Pi): x += 1
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
def subms(ms):
    c = Counter(ms); keys = sorted(c)
    for combo in itertools.product(*[range(c[k] + 1) for k in keys]):
        sub = tuple(k for k, m in zip(keys, combo) for _ in range(m))
        yield sub, prod(sub)
def kind_of(pa, pb, supp):
    # ratio r = pa/pb
    if pa == pb: return 'one'
    if pa == x * pb: return 'x'
    for (num, den, tag) in ((pa, pb, 'w'), (pb, pa, '1/w'), (pa, x * pb, 'xw'), (x * pb, pa, 'x/w')):
        if num % den == 0:
            w = num // den
            if w in Vset and w not in supp: return tag
    return None
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
    for Dm in facts(P, 2):
        if len(Dm) < 2: continue
        for Dp in facts(P * x, 2):
            if set(Dp) & set(Dm): continue
            st['rel'] += 1
            supp = set(Dp) | set(Dm); full = (len(Dp), len(Dm))
            best = None
            for A, pa in subms(Dp):
                for B, pb in subms(Dm):
                    la, lb = len(A), len(B)
                    if (la, lb) == (0, 0) or (la, lb) == full: continue
                    if best is not None and la + lb >= best[0]: continue
                    k = kind_of(pa, pb, supp)
                    if k: best = (la + lb, la, lb, k, A, B)
            if best is None:
                st['NONE'] += 1; print('NONE', Dp, Dm, flush=True); continue
            shapes[best[1:4]] += 1
            if best[0] >= 3 and len(ex) < 30: ex.append((Dp, Dm, best))
print('X', X, 'x', x, 'Pi', Pi, dict(st))
for k, v in sorted(shapes.items(), key=lambda t: -t[1]): print('  shape', k, v)
for e in ex: print('EX', e)
