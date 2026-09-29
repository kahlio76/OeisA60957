import random, sys
from sympy import divisors
from collections import defaultdict, Counter
exec('def reps'+open('badres.py').read().split('def reps')[1].split('random.seed')[0])
random.seed(int(sys.argv[1])); T=int(sys.argv[2])
st=Counter()
def key(e): return tuple(sorted(e.items()))
for trial in range(T):
    gens=random.sample(range(4,60),random.randint(1,3))
    W=set()
    for g in gens: W|=set(d for d in divisors(g) if d>1)
    # choose x not in W with all proper divisors in W
    cands=[x for x in range(4,200) if x not in W and all(d in W for d in divisors(x) if 1<d<x) and any(1<d<x for d in divisors(x))]
    if not cands: continue
    x=random.choice(cands)
    cap={v:random.randint(1,3) for v in W}
    full=reps(W,cap)
    for Mv,lst in full.items():
        if Mv*x*x not in full and Mv*x**3 not in full: continue
        t=2 if Mv*x*x in full else 3
        if Mv*x not in full: st['LFAIL']+=1; print('LFAIL',sorted(W),cap,x,Mv); continue
        # mechanism: Q + U with prod U = x ?
        tgt=set(key(e) for e in full[Mv*x])
        found=None
        for Q in lst:
            # add blocks U: product x, U a multiset of W elements; try pairs/single
            for d in divisors(x):
                if 1<d<x:
                    e=dict(Q); e[d]=e.get(d,0)+1; e[x//d]=e.get(x//d,0)+1
                    if key(e) in tgt: found='Q+split'; break
            if found: break
            for q in Q:
                for d in divisors(x):
                    if d>1 and q*d in W:
                        e=dict(Q); e[q]-=1
                        if e[q]==0: del e[q]
                        e[q*d]=e.get(q*d,0)+1
                        if d<x: e[x//d]=e.get(x//d,0)+1
                        if key(e) in tgt: found='Q merge'; break
                if found: break
            if found: break
        st[found or 'other']+=1
print(st)
