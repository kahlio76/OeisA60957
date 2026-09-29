# Is greedy(N*x) - greedy(N) always an M-adjacent bridge?  (framework B setting)
import sys
from collections import Counter
from sympy import isprime, primerange, factorint
from common import caps_real
from sigreedy_lib import suffix_sets, greedy_rep
from lexascent_lib import madj

N0, N1 = int(sys.argv[1]), int(sys.argv[2])
st = Counter(); shapes = Counter()
for n in range(N0, N1 + 1):
    for p in primerange(2, n + 1):
        for x in range(4, n + 1):
            if x % p == 0 or isprime(x):
                continue
            W, cap = caps_real(n, p, x)
            S = suffix_sets(W, cap)
            for N in S[0]:
                if N * x not in S[0]:
                    continue
                st['inst'] += 1
                Q = greedy_rep(N, W, cap, S); G = greedy_rep(N * x, W, cap, S)
                if madj(Q, G):
                    st['ok'] += 1
                    rem = sum(max(0, a - b) for a, b in zip(Q, G)); add = sum(max(0, b - a) for a, b in zip(Q, G))
                    shapes[(rem, add)] += 1
                else:
                    st['NO'] += 1
                    if st['NO'] <= 8:
                        print('NO', n, p, x, N, 'Q', {W[i]: c for i, c in enumerate(Q) if c}, 'G', {W[i]: c for i, c in enumerate(G) if c}, flush=True)
    print('n', n, dict(st), flush=True)
print(sorted(shapes.items())[:40])
