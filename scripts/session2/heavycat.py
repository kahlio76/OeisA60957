# (MC-cat-heavy) random test: in W_n (p-free numbers in [2,n], caps ell), generate random heavy positive parts
# D+ (sum over r of C(d_r,2) >= T0 + 2, d_r <= ell_r), enumerate factorizations of prod(D+) into D- (elements of
# W_n \ supp D+, multiplicities <= ell), and check for a certificate: proper part with ratio 1 or w^{+-1},
# w in W_n \ supp D.  Record the smallest certificate shape.  Parts searched by increasing size up to SMAX.
import sys, random, itertools
from math import prod
from collections import Counter
n = int(sys.argv[1]); p = int(sys.argv[2]); TRIALS = int(sys.argv[3]); FMAX = int(sys.argv[4]); SMAX = int(sys.argv[5])
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 1
random.seed(seed)
W = [s for s in range(2, n + 1) if s % p]
Wset = set(W)
ell = {}
for r in W:
    k = 0; v = r
    while v <= n: k += 1; v *= p
    ell[r] = k
L = 0
while p ** (L + 1) <= n: L += 1
T0 = L * (L + 1) // 2

def factorizations(P, allowed, limit):
    out = []; al = sorted(allowed)
    cnt = Counter()
    def rec(P, i, cur):
        if len(out) >= limit: return
        if P == 1: out.append(tuple(cur)); return
        for k in range(i, len(al)):
            s = al[k]
            if s > P: break
            if P % s == 0 and cnt[s] < ell[s]:
                cnt[s] += 1; cur.append(s); rec(P // s, k, cur); cur.pop(); cnt[s] -= 1
    rec(P, 0, [])
    return out

def certificate(Dp, Dm):
    supp = set(Dp) | set(Dm)
    cp, cm = Counter(Dp), Counter(Dm)
    full = (len(Dp), len(Dm))
    # enumerate sub-multisets by size
    kp, km = sorted(cp), sorted(cm)
    best = None
    for size in range(1, SMAX + 1):
        for a in range(0, size + 1):
            b = size - a
            if a > len(Dp) or b > len(Dm): continue
            for A in itertools.combinations_with_replacement(kp, a):
                ca = Counter(A)
                if any(ca[x] > cp[x] for x in ca): continue
                pa = prod(A)
                for B in itertools.combinations_with_replacement(km, b):
                    cb = Counter(B)
                    if any(cb[x] > cm[x] for x in cb): continue
                    if (a, b) == full: continue
                    pb = prod(B)
                    if pa == pb: return (a, b, 'one', A, B)
                    if pa % pb == 0 and pa // pb in Wset and pa // pb not in supp: return (a, b, 'w', A, B)
                    if pb % pa == 0 and pb // pa in Wset and pb // pa not in supp: return (a, b, '1/w', A, B)
    return None

st = Counter(); shapes = Counter()
cand = [r for r in W if ell[r] >= 2]
for trial in range(TRIALS):
    # build heavy D+
    Dp = []
    used = set()
    tot = 0
    tries = 0
    while tot < T0 + 2 and tries < 200:
        tries += 1
        r = random.choice(cand)
        if r in used: continue
        d = random.randint(2, ell[r])
        used.add(r); Dp += [r] * d; tot += d * (d - 1) // 2
    if tot < T0 + 2: continue
    for _ in range(random.randint(0, 2)):
        r = random.choice(W)
        if Counter(Dp)[r] < ell[r]: Dp.append(r)
    Dp.sort()
    P = prod(Dp)
    allowed = [s for s in W if s not in set(Dp)]
    for Dm in factorizations(P, allowed, FMAX):
        st['rel'] += 1
        c = certificate(Dp, list(Dm))
        if c is None:
            st['NOCERT_upto_' + str(SMAX)] += 1
            print('NOCERT', 'n', n, 'p', p, 'D+', Dp, 'D-', Dm, flush=True)
        else:
            shapes[c[:3]] += 1
print('n', n, 'p', p, 'L', L, 'T0', T0, dict(st))
for k, v in sorted(shapes.items(), key=lambda t: -t[1]): print('  shape', k, v)
