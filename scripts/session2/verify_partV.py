# Independent verification of the Part V counterexamples in PROOF.md.
from itertools import product
from collections import Counter

def world(n, p, x):
    W = [s for s in range(2, x) if s % p]
    cap = {}
    for s in W:
        k, v = 0, s
        while v <= n:
            k += 1; v *= p
        cap[s] = k
    return W, cap

def reps(M, W, cap):
    """all reps of M over W (dict form), plain DFS"""
    out = []
    def rec(i, rem, cur):
        if rem == 1:
            out.append(dict(cur)); return
        if i == len(W): return
        s = W[i]; v = 1
        for j in range(cap[s] + 1):
            if j:
                v *= s
                if rem % v: break
            if j: cur[s] = j
            rec(i + 1, rem // v, cur)
            if j: del cur[s]
    rec(0, M, {})
    return out

def lexmax_small(M, W, cap):
    R = reps(M, W, cap)
    return max(R, key=lambda e: tuple(e.get(s, 0) for s in W))

def madj(e, f):
    keys = set(e) | set(f)
    up = sum(1 for k in keys if f.get(k, 0) - e.get(k, 0) >= 2)
    dn = sum(1 for k in keys if e.get(k, 0) - f.get(k, 0) >= 2)
    return up <= 1 and dn <= 1

def prod(e):
    r = 1
    for k, c in e.items(): r *= k ** c
    return r

# 1. greedy(Nx) - greedy(N) not M-adjacent
n, p, x, N = 50, 5, 18, 832
W, cap = world(n, p, x)
Q = lexmax_small(N, W, cap); G = lexmax_small(N * x, W, cap)
print('CE1 caps', {s: cap[s] for s in W}, '\n Q', Q, prod(Q) == N, '\n G', G, prod(G) == N * x, '\n M-adj?', madj(Q, G))
print(' bridge Q+[3]+[6] valid?', all(Q.get(s, 0) + (1 if s in (3, 6) else 0) <= cap[s] for s in W))

# 2. greedy Q has no M-adjacent rep of Nx
n, p, x, N = 42, 3, 16, 40140800
W, cap = world(n, p, x)
Q = lexmax_small(N, W, cap); RX = reps(N * x, W, cap)
print('CE2 caps', {s: cap[s] for s in W}, '\n Q', Q, '\n reps of Nx', RX, '\n any M-adj?', any(madj(Q, X) for X in RX))
Qp = {2: 3, 4: 2, 8: 2, 10: 1, 14: 1, 5: 1, 7: 1}
print(' Qp is rep of N?', prod(Qp) == N and all(Qp[s] <= cap[s] for s in Qp), ' M-adj to X?', madj(Qp, RX[0]))

# 3. Lemma-L instance where greedy admits no simple insertion
n, p, x, N = 242, 11, 15, 2939328
W, cap = world(n, p, x)
Q = lexmax_small(N, W, cap)
print('CE3 caps>1', {s: cap[s] for s in W if cap[s] > 1}, '\n Q', Q, prod(Q) == N)
print(' N*x^2 representable?', len(reps(N * x * x, W, cap)) > 0, ' N*x representable?', len(reps(N * x, W, cap)) > 0)
# simple insertion: x=15=3*5: host for 3 in {1}U supp Q with 3h in W & room; host for 5 similarly
def simple(Q):
    for (d1, d2) in [(3, 5)]:
        hosts = [1] + [s for s in Q if Q[s] > 0]
        for h1 in hosts:
            for h2 in hosts:
                e = dict(Q); ok = True
                for d, h in ((d1, h1), (d2, h2)):
                    v = d * h
                    if v not in cap: ok = False; break
                    if h != 1:
                        if e.get(h, 0) < 1: ok = False; break
                        e[h] -= 1
                    e[v] = e.get(v, 0) + 1
                    if e[v] > cap[v]: ok = False; break
                if ok: return True
    return False
print(' simple insertion exists?', simple(Q))
Q2 = dict(Q); Q2[2] -= 2; Q2[12] = Q2.get(12, 0) + 1; Q2[5] = Q2.get(5, 0) + 1
print(' merge-host move Q-2[2]+[12]+[5] valid rep of Nx?', prod({k: v for k, v in Q2.items() if v}) == N * x and all(Q2[s] <= cap[s] for s in Q2 if Q2[s]))
