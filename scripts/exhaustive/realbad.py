import sys
from sympy import primerange
from math import comb
from collections import defaultdict, Counter
N0=int(sys.argv[1]); N=int(sys.argv[2])
def allreps(m,p):
    U=[r for r in range(2,m+1) if r%p]
    ell={}
    for r in U:
        k=0;x=r
        while x<=m:k+=1;x*=p
        ell[r]=k
    reps=defaultdict(list); reps[1].append({})
    for r in U:
        nr=defaultdict(list)
        for R,lst in reps.items():
            for e in range(0,ell[r]+1):
                for d in lst:
                    if e: dd=dict(d); dd[r]=e
                    else: dd=d
                    nr[R*r**e].append(dd)
        reps=nr
    return reps,ell
st=Counter()
for n in range(N0,N+1):
    for p in primerange(2,n):
        r=n;k=0
        while r%p==0: r//=p;k+=1
        if r==1: continue
        G=n-1
        reps,ell=allreps(G,p)
        L0=0;x=1
        while x*p<=G: x*=p;L0+=1
        T0=L0*(L0+1)//2
        for A,lst in reps.items():
            if A*r not in reps: continue
            if k>=1 and any(e.get(r,0)<k for e in lst): continue
            flst=reps[A*r]
            def c1(e,f): return sum(comb(e.get(s,0)-f.get(s,0),2) for s in e if e.get(s,0)>f.get(s,0))
            best1=min(c1(e,f) for e in lst for f in flst)
            best2=min(c1(f,e) for e in lst for f in flst)
            ok1=best1<=T0-k+1; ok2=best2<=T0+k+1
            st[(k>0,ok1,ok2)]+=1
            if not(ok1 and ok2):
                print('FAIL n=%d p=%d r=%d k=%d A=%d T0=%d best1=%d best2=%d'%(n,p,r,k,A,T0,best1,best2),flush=True)
    print('done',n,dict(st),flush=True)
