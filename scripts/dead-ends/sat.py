# test lemma: S "simple-saturated" (every p-chain chosen set is a top segment, chain-1 contains p..p^L) => v(S) = max over T with same p-free part
import sys
from sympy import primerange
from itertools import combinations
def vp(x,p):
    v=0
    while x%p==0: x//=p; v+=1
    return v
for n in range(3,int(sys.argv[1])+1):
    for p in primerange(2,n+1):
        # compute max v for each R via DP over elements: dict R -> max v
        best={1:0}
        for x in range(2,n+1):
            v=vp(x,p); r=x//p**v
            nb=dict(best)
            for R,vv in best.items():
                k=R*r
                if nb.get(k,-1)<vv+v: nb[k]=vv+v
            best=nb
        # enumerate simple-saturated S: per chain choose count c, top segment. chains r (p∤r, r<=n)
        chains=[r for r in range(1,n+1) if r%p]
        L={r:0 for r in chains}
        for r in chains:
            while r*p**(L[r]+1)<=n: L[r]+=1
        # enumerate count vectors recursively (could be large); limit n
        bad=0; total=0
        def rec(i,R,v):
            global bad,total
            if i==len(chains):
                total+=1
                if best[R]!=v:
                    bad+=1
                    if bad<=3: print('NON-MAX saturated n=%d p=%d R=%d v=%d max=%d'%(n,p,R,v,best[R]))
                return
            r=chains[i]; Lr=L[r]
            opts=range(0,Lr+2)
            if r==1: opts=[Lr, Lr+1] if Lr>=1 else [0,1]   # chain 1 must contain p..p^L (levels1..L); level0 (element 1) optional
            for c in opts:
                if r==1:
                    vv=Lr*(Lr+1)//2; RR=R
                else:
                    vv=sum(Lr-j for j in range(c)); RR=R*r**c
                rec(i+1,RR,v+vv)
        rec(0,1,0)
        if bad: print('n=%d p=%d saturated=%d nonmax=%d'%(n,p,total,bad))
    print('done',n,flush=True)
