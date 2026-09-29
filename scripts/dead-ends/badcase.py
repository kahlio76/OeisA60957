import sys
from sympy import primerange
from collections import defaultdict
N=int(sys.argv[1])
INF=10**9
for p in primerange(2,N+1):
    cnt=defaultdict(int)
    for n in range(2,N+1):
        t=0; s=n
        while s%p==0: s//=p; t+=1
        if s==1: continue
        m=n-1
        U=[r for r in range(1,m+1) if r%p]
        ell={}
        for r in U:
            k=0;x=r
            while x<=m:k+=1;x*=p
            ell[r]=k
        # DP: R -> (min count of chain s)
        best={1:0}
        for r in U:
            nb={}
            for R,v in best.items():
                for e in range(0,ell[r]+1):
                    RR=R*r**e if r>1 else R
                    vv=v+(e if r==s else 0)
                    if RR not in nb or vv<nb[RR]: nb[RR]=vv
            best=nb
        ls=ell.get(s,0)  # = t
        for Rs,v in best.items():   # Rs = R/s
            R=Rs*s
            if v==ls and R in best:   # all reps of R/s fill chain s, and old reps of R exist
                cnt['t=%d'%t]+=1
                if cnt['t=%d'%t]<=2: print('BAD p=%d n=%d s=%d t=%d R=%d'%(p,n,s,t,R))
    print('p=%d'%p,dict(cnt),flush=True)
