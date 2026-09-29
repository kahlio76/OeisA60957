import sys
from sympy import primerange, primefactors
from collections import defaultdict
N=int(sys.argv[1])
def allreps(m,p):
    U=[r for r in range(2,m+1) if r%p]
    ell={}
    for r in U:
        k=0;x=r
        while x<=m:k+=1;x*=p
        ell[r]=k
    reps=defaultdict(list); reps[1].append(())
    for r in U:
        nr=defaultdict(list)
        for R,lst in reps.items():
            for e in range(0,ell[r]+1):
                for d in lst: nr[R*r**e].append(d+((r,e),) if e else d)
        reps=nr
    return reps,ell
def key(e): return sorted([r for r,c in e for _ in range(c)],reverse=True)
for m in range(3,N+1):
    for p in primerange(2,m+1):
        reps,ell=allreps(m,p); stuck=0
        for R,lst in reps.items():
            if len(lst)<2: continue
            top=max(key(e) for e in lst)
            for e in lst:
                if key(e)==top: continue
                c=dict(e); ok=False
                parts=list(c)
                for x in parts:
                    for q in primefactors(x):
                        for y in parts:
                            if y<x or (y==x and c[x]<2): continue
                            if y*q>m: continue
                            d=dict(c); d[x]-=1; d[y]-=1
                            nx=x//q; ny=y*q
                            if nx>1: d[nx]=d.get(nx,0)+1
                            d[ny]=d.get(ny,0)+1
                            if all(v<=ell[k] for k,v in d.items() if v>0): ok=True;break
                        if ok:break
                    if ok:break
                if not ok:
                    stuck+=1
                    if stuck<=2: print('NO TRANSFER m=%d p=%d R=%d e=%s top=%s'%(m,p,R,key(e),top))
        if stuck: print('m=%d p=%d stuck=%d'%(m,p,stuck),flush=True)
    print('checked',m,flush=True)
