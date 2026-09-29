# (Energy): for W_n (p-free numbers in [2,n], caps ell_r) and every p-free R, the energies
# E(g) = sum_r C(g_r, 2) over reps g of R have no gap larger than T0 + 1 (T0 = L(L+1)/2).
import sys
from collections import Counter
from sympy import primerange
from sigreedy_lib import suffix_sets
from profscan_lib import caps_for, all_reps_of

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
REPMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        W = [s for s in range(2, n + 1) if s % p]
        cap = caps_for(W, p, n)
        L = 0
        while p ** (L + 1) <= n: L += 1
        T0 = L * (L + 1) // 2
        S = suffix_sets(W, cap)
        st = Counter(); worst = (0, None)
        for R in S[0]:
            reps = all_reps_of(R, W, cap, S)
            if len(reps) > REPMAX: st['skip'] += 1; continue
            Es = sorted({sum(c * (c - 1) // 2 for c in g) for g in reps})
            gap = max((b - a for a, b in zip(Es, Es[1:])), default=0)
            if gap > worst[0]: worst = (gap, R)
            if gap > T0 + 1:
                st['ENERGY_GAP'] += 1
        print('n', n, 'p', p, 'T0', T0, 'worst gap', worst, dict(st), flush=True)
