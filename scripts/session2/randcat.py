# Random search for counterexamples to (MC-cat) in larger worlds V = V(X, Pi):
# D+ = 2[y1] + 2[y2] + (0..EXTRA random elements), D- ranges over all factorizations of prod(D+) into
# elements of V \ supp(D+).  For each primitive (no proper ratio-1 part) D, look for a single-catalyst part.
import sys, random, itertools
from math import prod
from collections import Counter
X = int(sys.argv[1]); TRIALS = int(sys.argv[2]); EXTRA = int(sys.argv[3])
Pi = tuple(int(t) for t in sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[4] != '-' else ()
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
FMAX = int(sys.argv[6]) if len(sys.argv) > 6 else 3000
random.seed(seed)
V = [s for s in range(2, X) if all(s % q for q in Pi)]
Vset = set(V)

def factorizations(P, allowed, limit):
    out = []
    al = sorted(allowed)
    def rec(P, i, cur):
        if len(out) >= limit: return
        if P == 1: out.append(tuple(cur)); return
        for k in range(i, len(al)):
            s = al[k]
            if s > P: break
            if P % s == 0:
                cur.append(s); rec(P // s, k, cur); cur.pop()
    rec(P, 0, [])
    return out

def subms(ms):
    c = Counter(ms); keys = sorted(c)
    for combo in itertools.product(*[range(c[k] + 1) for k in keys]):
        yield len([1 for k, m in zip(keys, combo) for _ in range(m)]), prod(k ** m for k, m in zip(keys, combo))

st = Counter()
for trial in range(TRIALS):
    y1, y2 = random.sample(V, 2)
    Dp = [y1, y1, y2, y2] + [random.choice(V) for _ in range(random.randint(0, EXTRA))]
    P = prod(Dp)
    allowed = [s for s in V if s not in set(Dp)]
    for Dm in factorizations(P, allowed, FMAX):
        st['rel'] += 1
        supp = set(Dp) | set(Dm); full = (len(Dp), len(Dm))
        SP = list(subms(Dp)); SM = list(subms(Dm))
        prim = True; cat = False
        for la, pa in SP:
            for lb, pb in SM:
                if (la, lb) == (0, 0) or (la, lb) == full: continue
                if pa == pb: prim = False; break
                if not cat:
                    if pa % pb == 0 and pa // pb in Vset and pa // pb not in supp: cat = True
                    elif pb % pa == 0 and pb // pa in Vset and pb // pa not in supp: cat = True
            if not prim: break
        if not prim: continue
        st['prim'] += 1
        if not cat:
            st['NOCAT'] += 1
            print('NOCAT X', X, 'D+', sorted(Dp), 'D-', sorted(Dm), flush=True)
print('X', X, 'Pi', Pi, dict(st), flush=True)
