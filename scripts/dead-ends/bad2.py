import sys
from sympy import primerange
N=int(sys.argv[1])
for p in primerange(2,N//2+1):
    cnt={}
    for n in range(2,N+1):
        t=0;s=n
        while s%p==0: s//=p; t+=1
        if s==1 or t==0: continue
        m=n-1
        U=[r for r in range(2,m+1) if r%p]
        ell={}
        for r in U:
            k=0;x=r
            while x<=m:k+=1;x*=p
            ell[r]=k
        best={1:0}   # R -> min count at chain s
        for r in U:
            nb={}
            for R,v in best.items():
                for e in range(0,ell[r]+1):
                    RR=R*r**e; vv=v+(e if r==s else 0)
                    if RR not in nb or vv<nb[RR]: nb[RR]=vv
            best=nb
        for Rs,v in best.items():
            if v==t and Rs*s in best:
                key=(s,t); cnt[key]=cnt.get(key,0)+1
    print('p=%d bad(t>=1) by (s,t):'%p,cnt,flush=True)
