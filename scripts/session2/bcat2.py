# Search for relations D (prod D+ = prod D-, disjoint supports, elements of V = V(X,Pi)) that are
#   primitive-ish: no proper conformal part with ratio 1,
#   catalyst-free: no proper conformal part with ratio z or 1/z, z in V \ supp(D),
#   and NOT M-adjacent.
# Such D would refute (MC-cat).  Also optional ratio-x mode for (B-cat): prod D+ = x * prod D-.
import sys, itertools
from math import prod
from collections import Counter, defaultdict
from sympy import primerange, factorint

X = int(sys.argv[1]); PMAX = int(sys.argv[2]); Pi = tuple(int(t) for t in sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] != '-' else ()
MODE = sys.argv[4] if len(sys.argv) > 4 else 'mc'   # 'mc' or 'b' (ratio x = next element)
V = [s for s in range(2, X) if all(s % q for q in Pi)]
Vset = set(V)
xnext = X
while any(xnext % q == 0 for q in Pi): xnext += 1

# factorizations of P into parts from V (nondecreasing)
memo = {}
def facts(P, minpart):
    key = (P, minpart)
    if key in memo: return memo[key]
    out = []
    if P == 1:
        out = [()]
    else:
        for s in V:
            if s < minpart: continue
            if s > P: break
            if P % s == 0:
                for rest in facts(P // s, s):
                    out.append((s,) + rest)
    memo[key] = out
    return out

def madj_ms(Dp, Dm):
    cp = Counter(Dp); cm = Counter(Dm)
    return sum(1 for v in cp.values() if v >= 2) <= 1 and sum(1 for v in cm.values() if v >= 2) <= 1

def submultisets(ms):
    c = Counter(ms); keys = sorted(c)
    for combo in itertools.product(*[range(c[k] + 1) for k in keys]):
        yield tuple(k for k, m in zip(keys, combo) for _ in range(m)), prod(k ** m for k, m in zip(keys, combo))

st = Counter(); found = 0
# candidate products P: all P <= PMAX that are products of V elements
cands = set([1])
frontier = [1]
allP = set()
for s in V:
    new = set()
    for v in list(cands):
        w = v * s
        while w <= PMAX * (xnext if MODE == 'b' else 1):
            new.add(w); w *= s
    cands |= new
Ps = sorted(cands)
for P in Ps:
    if P == 1 or P > PMAX: continue
    F = facts(P, 2)
    if len(F) < 2 and MODE == 'mc': continue
    if MODE == 'mc':
        pairs = [(F[i], F[j]) for i in range(len(F)) for j in range(len(F)) if i != j]
    else:
        G = facts(P * xnext, 2)
        pairs = [(g, f) for g in G for f in F]   # D+ = g (product P*x), D- = f (product P)
    for Dp, Dm in pairs:
        if MODE == 'mc' and Dp > Dm: continue  # each unordered pair once (sign symmetry)
        if set(Dp) & set(Dm): continue
        st['rel'] += 1
        if len(Dm) < 2: continue
        st['dminus>=2'] += 1
        supp = set(Dp) | set(Dm)
        subsP = list(submultisets(Dp)); subsM = list(submultisets(Dm))
        ok = True
        full = (len(Dp), len(Dm))
        target_ratio_num = xnext if MODE == 'b' else 1
        for A, pa in subsP:
            for B, pb in subsM:
                if (len(A), len(B)) == (0, 0) or (len(A), len(B)) == full: continue
                # ratio of part (A,B) = pa/pb ; complement ratio = target/(pa/pb)
                for num, den in ((pa, pb), (target_ratio_num * pb, pa)):
                    # check ratio num/den in {1} or {z, 1/z : z in V \ supp}; in b-mode the ratio-1 condition applies to
                    # the complement part too (parts with ratio x are also "moves")
                    if num == den: ok = False; break
                    if num % den == 0 and (num // den) in Vset and (num // den) not in supp: ok = False; break
                    if den % num == 0 and (den // num) in Vset and (den // num) not in supp: ok = False; break
                if not ok: break
            if not ok: break
        if ok:
            found += 1
            st['CATFREE_DM2'] += 1
            if found <= 25:
                print('FOUND X', X, 'Pi', Pi, 'mode', MODE, 'D+', Dp, 'D-', Dm, flush=True)
print('X', X, 'Pi', Pi, 'mode', MODE, 'PMAX', PMAX, dict(st), flush=True)
