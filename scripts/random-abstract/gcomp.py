import random, sys
from sympy import divisors
from collections import defaultdict
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); B=int(sys.argv[3]); maxcap=int(sys.argv[4])
bad=0; tested=0
for t in range(T):
    gens=random.sample(range(2,B),random.randint(1,4))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    V=sorted(V)
    cap={v:random.randint(1,maxcap) for v in V}
    S={1}
    for v in V: S={x*v**j for x in S for j in range(cap[v]+1)}
    Sset=S
    for s in range(4,B*2):
        ds=[d for d in divisors(s) if 1<d<s]
        if not ds or any(d not in V for d in ds): continue
        tested+=1
        for x in Sset:
            if x%s==0: continue
            # x not divisible by s: walk multiples
            js=[j for j in range(0,12) if x*s**j in Sset]
            if js and max(js)-min(js)+1!=len(js):
                bad+=1
                if bad<=5: print('FAIL s=%d inV=%s V=%s cap=%s x=%d js=%s'%(s,s in V,V,cap,x,js),flush=True)
                break
print('bad',bad,'tested',tested)
