import random, sys
from sympy import primerange, divisors
from collections import defaultdict
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
def check(D,p):
    V=defaultdict(set); V[1].add(0)
    for x in sorted(D):
        if x==1: continue
        v=vp(x,p); u=x//p**v
        new=defaultdict(set)
        for R,s in V.items():
            new[R]|=s; new[R*u]|={a+v for a in s}
        V=new
    for R,s in V.items():
        if max(s)-min(s)+1!=len(s): return R,sorted(s)
    return None
random.seed(int(sys.argv[1]))
bad=0
for trial in range(int(sys.argv[2])):
    # random divisor-closed set: generate by random generators up to bound
    B=random.choice([20,30,40,60]); gens=random.sample(range(2,B),random.randint(2,5))
    D=set()
    for g in gens: D|=set(divisors(g))
    for p in [q for q in primerange(2,B) if any(x%q==0 for x in D)]:
        r=check(D,p)
        if r:
            bad+=1
            if bad<=5: print('COUNTEREX p=%d D=%s R=%d V=%s'%(p,sorted(D),r[0],r[1]))
            break
print('bad',bad)
