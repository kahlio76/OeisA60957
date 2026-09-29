import random, sys
from sympy import divisors, factorint, primerange
from collections import defaultdict
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); B=int(sys.argv[3]); maxcap=int(sys.argv[4])
def check(V,cap):
    S={1}
    for v in V:
        S={x*v**j for x in S for j in range(cap[v]+1)}
    for q in primerange(2,B+1):
        fib=defaultdict(set)
        for x in S:
            e=0;y=x
            while y%q==0:y//=q;e+=1
            fib[y].add(e)
        for y,E in fib.items():
            if max(E)-min(E)+1!=len(E): return q,y,sorted(E)
    return None
bad=0
for t in range(T):
    gens=random.sample(range(2,B),random.randint(1,4))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    V=sorted(V)
    cap={v:random.randint(1,maxcap) for v in V}
    r=check(V,cap)
    if r:
        bad+=1
        if bad<=5: print('FAIL',V,cap,r,flush=True)
print('bad',bad,'of',T)
