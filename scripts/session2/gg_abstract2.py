# (GG) in abstract worlds: W = {s in [2, X) : gcd(s, Pi) = 1}, x = smallest composite >= X coprime to Pi
# (or any composite coprime to Pi that is > all of W), caps random non-increasing (mode 'mono') or
# arbitrary (mode 'arb'). Test: greedy(N*x) - greedy(N) M-adjacent whenever both representable.
# Also test (GL): N*x^t in S (t>=2) => greedy(N) admits simple insertion.
import sys, random
from collections import Counter
from sympy import primerange, isprime, factorint
from sigreedy_lib import suffix_sets, greedy_rep
from simple_ins_lib import simple_insert
from lexascent_lib import madj

seed, T, Xmax, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
random.seed(seed)
st = Counter()
for trial in range(T):
    primes = list(primerange(2, Xmax))
    Pi = set(random.sample(primes, random.randint(0, min(2, len(primes) - 1))))
    xs = [x for x in range(4, Xmax + 1) if all(x % q for q in Pi) and not isprime(x)]
    if not xs:
        continue
    x = random.choice(xs)
    W = [s for s in range(2, x) if all(s % q for q in Pi)]
    if not W:
        continue
    if mode == 'mono':
        # random non-increasing caps
        caps = sorted([random.choice([1, 1, 1, 2, 2, 3]) for _ in W], reverse=True)
    else:
        caps = [random.choice([1, 1, 2, 3]) for _ in W]
    cap = dict(zip(W, caps))
    try:
        S = suffix_sets(W, cap)
    except MemoryError:
        continue
    if len(S[0]) > 400000:
        continue
    idx = {w: i for i, w in enumerate(W)}
    for N in S[0]:
        if N * x in S[0]:
            st['GG_inst'] += 1
            Q = greedy_rep(N, W, cap, S); G = greedy_rep(N * x, W, cap, S)
            if not madj(Q, G):
                st['GG_FAIL'] += 1
                if st['GG_FAIL'] <= 5:
                    print('GG_FAIL Pi', sorted(Pi), 'x', x, 'cap', cap, 'N', N,
                          {W[i]: c for i, c in enumerate(Q) if c}, {W[i]: c for i, c in enumerate(G) if c}, flush=True)
        if any(N * x**t in S[0] for t in range(2, 6)):
            st['GL_inst'] += 1
            Q = greedy_rep(N, W, cap, S)
            if not simple_insert(Q, W, idx, cap, x):
                st['GL_FAIL'] += 1
                if st['GL_FAIL'] <= 5:
                    print('GL_FAIL Pi', sorted(Pi), 'x', x, 'cap', cap, 'N', N, {W[i]: c for i, c in enumerate(Q) if c}, flush=True)
print(dict(st))
