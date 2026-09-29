# Lemma L locality probe (real setting).
# For each instance (n,p,x,N) with N and N*x^t representable (t>=2), and EVERY rep Q of N,
# compute min distance from Q to a rep of N*x.  Report worst case.
import sys
from collections import Counter
from sympy import isprime, primerange
from common import caps_real, all_reps, dist

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
worst = Counter()
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        for x in range(4, n + 1):
            if x % p == 0 or isprime(x):
                continue
            W, cap = caps_real(n, p, x)
            reps = all_reps(W, cap)
            for N, QL in reps.items():
                if not any(N * x**t in reps for t in range(2, 8)):
                    continue
                XL = reps.get(N * x)
                if XL is None:
                    print('LFAIL', n, p, x, N); continue
                mx = 0; arg = None
                for Q in QL:
                    d = min(dist(Q, Y) for Y in XL)
                    if d > mx:
                        mx = d; arg = Q
                worst[mx] += 1
                if mx >= 4:
                    print('far', n, p, x, N, 'Q=', {W[i]: c for i, c in enumerate(arg) if c}, 'd=', mx)
    print('n', n, dict(sorted(worst.items())), flush=True)
