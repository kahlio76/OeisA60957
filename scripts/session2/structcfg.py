# Structured (p-cat) configurations (PROOF.md Lemma 6.6): for each p-free r>=2 choose alpha_r (bottom segment in D+)
# and m_r (top segment in D-), alpha_r + m_r <= ell_r; pure chain in D-.  Balance prod r^alpha = prod r^m, t >= 2.
# Enumerate (DFS over primes, descending) and, for each, test whether a certificate exists, using the exact
# interval characterisation over sub-balances with at most one catalyst.  Report configurations with NO certificate
# (these would be counterexamples to (p-cat)), and statistics of which certificate types occur.
import sys, itertools
from collections import Counter, defaultdict
from sympy import primerange, factorint

n = int(sys.argv[1]); p = int(sys.argv[2]); LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6
L = 0
while p ** (L + 1) <= n: L += 1
T0 = L * (L + 1) // 2
R = [r for r in range(2, n + 1) if r % p]
ell = {}
for r in R:
    k = 0; v = r
    while v <= n: k += 1; v *= p
    ell[r] = k
fac = {r: factorint(r) for r in R}
primes = sorted({q for r in R for q in fac[r]}, reverse=True)
# assign each chain to its largest prime factor
by_top = defaultdict(list)
for r in R: by_top[max(fac[r])].append(r)

configs = []
def dfs(pi, choice, bal):
    if len(configs) >= LIMIT: return
    if pi == len(primes):
        if all(v == 0 for v in bal.values()):
            configs.append(dict(choice))
        return
    q = primes[pi]
    chains = by_top[q]
    # enumerate choices for chains whose largest prime is q
    opts = []
    for r in chains:
        opts.append([(a, m) for a in range(ell[r] + 1) for m in range(ell[r] + 1 - a)])
    for combo in itertools.product(*opts):
        nb = dict(bal)
        for r, (a, m) in zip(chains, combo):
            for qq, e in fac[r].items():
                nb[qq] = nb.get(qq, 0) + e * (a - m)
        if nb.get(q, 0) != 0: continue
        for r, am in zip(chains, combo): choice[r] = am
        dfs(pi + 1, choice, nb)
        for r in chains: choice.pop(r, None)
        if len(configs) >= LIMIT: return
dfs(0, {}, {})

def tval(cfg):
    t = -T0
    for r, (a, m) in cfg.items():
        t += a * (a - 1) // 2
        t -= sum(range(ell[r] - m, ell[r]))
    return t

st = Counter(); shown = 0
for cfg in configs:
    t = tval(cfg)
    if t < 2: continue
    st['t>=2'] += 1
    # certificate search: sub-balances c+ <= a, c- <= m, with optional catalyst w = s * p^g, s p-free, g free level of s
    # (free level: g in [alpha_s, ell_s - m_s)), or s = 1? (pure powers all in D-, not free).
    act = [r for r, (a, m) in cfg.items() if a or m]
    # enumerate sub-balances by DFS over act with bounded counts; imbalance vector allowed = p-free part of a catalyst
    found = [False]
    # precompute level-sum ranges
    def plus_range(r, c):
        a = cfg[r][0]
        return (c * (c - 1) // 2, c * (a - 1) - c * (c - 1) // 2)
    def minus_range(r, c):
        a, m = cfg[r]; b = ell[r] - m
        return (c * b + c * (c - 1) // 2, c * (ell[r] - 1) - c * (c - 1) // 2)
    # free catalysts: map p-free s -> list of free levels
    freelev = {}
    for s in R:
        a, m = cfg.get(s, (0, 0))
        fl = list(range(a, ell[s] - m))
        if fl: freelev[s] = fl
    # DFS
    counts = {}
    def rec(i, imb, lo, hi):
        if found[0]: return
        if i == len(act):
            # imb: dict prime->exponent of (prod A / prod B) p-free part
            key = 1
            if any(v < 0 for v in imb.values()) and any(v > 0 for v in imb.values()): return
            s = 1
            for qq, e in imb.items(): s *= qq ** abs(e)
            sign = 1 if any(v > 0 for v in imb.values()) else (-1 if any(v < 0 for v in imb.values()) else 0)
            L0, H0 = lo - T0, hi   # pure-chain subset subtracts [0, T0]
            if sign == 0:
                if H0 >= 1 and L0 <= t - 1: found[0] = True
                return
            if s not in freelev: return
            for g in freelev[s]:
                # sign>0: prodA = p^k * (s p^g) * prodB -> k = delta - g ; sign<0: w*prodA = p^k prodB -> k = delta + g
                sh = -g if sign > 0 else g
                if H0 + sh >= 1 and L0 + sh <= t - 1: found[0] = True; return
            return
        r = act[i]; a, m = cfg[r]
        for cp in range(a + 1):
            for cm in range(m + 1):
                nb = dict(imb)
                for qq, e in fac[r].items():
                    nb[qq] = nb.get(qq, 0) + e * (cp - cm)
                    if nb[qq] == 0: del nb[qq]
                pl, ph = plus_range(r, cp) if cp else (0, 0)
                ml, mh = minus_range(r, cm) if cm else (0, 0)
                rec(i + 1, nb, lo + pl - mh, hi + ph - ml)
                if found[0]: return
    rec(0, {}, 0, 0)
    if found[0]: st['cert'] += 1
    else:
        st['NOCERT'] += 1
        if shown < 5:
            shown += 1
            print('NOCERT n', n, 'p', p, 't', t, {r: am for r, am in cfg.items() if am != (0, 0)}, flush=True)
print('n', n, 'p', p, 'L', L, 'configs', len(configs), dict(st), flush=True)
