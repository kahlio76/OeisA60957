# For lex-ascent (prefer small), find for each non-top rep e the minimal-L1 lex-greater M-adjacent rep f.
# Classify the move (removed multiset -> added multiset). Report hardest cases.
import sys
from collections import Counter
from sympy import primerange
from common import all_reps
from lexascent_lib import madj

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
show = int(sys.argv[3]) if len(sys.argv) > 3 else 6
st = Counter(); shapes = Counter(); examples = {}
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        W = [s for s in range(2, n + 1) if s % p]
        cap = {}
        for s in W:
            k = 0; v = s
            while v <= n:
                k += 1; v *= p
            cap[s] = k
        reps = all_reps(W, cap)
        for N, lst in reps.items():
            if len(lst) == 1:
                continue
            top = max(lst)
            for e in lst:
                if e == top:
                    continue
                best = None
                for f in lst:
                    if f > e and madj(e, f):
                        d = sum(abs(a - b) for a, b in zip(e, f))
                        if best is None or d < best[0]:
                            best = (d, f)
                if best is None:
                    st['STUCK'] += 1; continue
                d, f = best
                rem = tuple(sorted((W[i], e[i] - f[i]) for i in range(len(W)) if e[i] > f[i]))
                add = tuple(sorted((W[i], f[i] - e[i]) for i in range(len(W)) if f[i] > e[i]))
                shape = (sum(c for _, c in rem), sum(c for _, c in add))
                shapes[shape] += 1
                if shape not in examples or len(examples[shape]) < show:
                    examples.setdefault(shape, []).append((n, p, N, {W[i]: c for i, c in enumerate(e) if c}, rem, add))
    print('n', n, 'shapes (removed,added):', dict(sorted(shapes.items())), dict(st), flush=True)
for sh, ex in sorted(examples.items()):
    if sh[0] + sh[1] >= 4:
        print('shape', sh)
        for x in ex: print('   ', x)
