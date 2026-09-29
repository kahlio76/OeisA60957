# Print (Bb)/(Ba) instances whose best witness distance is > 3, with the witness pair.
import sys, itertools
from sympy import primerange, isprime
from sigreedy_lib import suffix_sets
from profscan_lib import all_reps_of
n, p, SHOW = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
k = n // p
def world(j, M):
    W = list(range(2, j + 1)) + sorted(M) + [s for s in range(k + 1, n + 1) if s % p]
    return W, {s: (2 if s <= j else 1) for s in W}
def A(g, W, j): return sum(1 for i, c in enumerate(g) if c == 2 and W[i] <= j)
def show(W, g): return {W[i]: c for i, c in enumerate(g) if c}
cnt = 0
for j in range(1, k + 1):
    mids = list(range(j + 1, k + 1))
    for m in range(len(mids) + 1):
        for M in itertools.combinations(mids, m):
            tasks = []
            if j + 1 <= k and j + 1 not in M: tasks.append(('b', j + 1, set(M), j + 1, 2))
            for x in mids:
                if x not in M: tasks.append(('a', j, set(M) | {x}, x, 1))
            for kind, jj, MM, item, lim in tasks:
                W, cap = world(jj, MM); S = suffix_sets(W, cap); it = W.index(item)
                for R in S[0]:
                    reps = all_reps_of(R, W, cap, S)
                    if len(reps) > 800: continue
                    new = [g for g in reps if g[it] == lim]; old = [g for g in reps if g[it] < lim]
                    if not new or not old: continue
                    best = min(((sum(abs(a - b) for a, b in zip(g, h)), g, h) for g in new for h in old
                                if abs(A(g, W, jj) - A(h, W, jj)) <= 2), key=lambda t: t[0])
                    if best[0] > 3 and cnt < SHOW:
                        cnt += 1
                        d, g, h = best
                        print(kind, 'j', jj, 'M', sorted(MM), 'item', item, 'R', R, 'd', d)
                        print('   new', show(W, g), 'A', A(g, W, jj))
                        print('   old', show(W, h), 'A', A(h, W, jj))
                        diff = {W[i]: g[i] - h[i] for i in range(len(W)) if g[i] != h[i]}
                        print('   new-old', diff, flush=True)
