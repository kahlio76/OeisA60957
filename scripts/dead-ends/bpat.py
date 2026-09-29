import sys
from sympy import primerange
from collections import defaultdict, Counter
N=int(sys.argv[1])
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
                    dd=dict(d)
                    if e: dd[r]=e
                    nr[R*r**e].append(dd)
        reps=nr
    return reps
def diff(f,e):
    keys=set(f)|set(e); rem=[];add=[]; p2=m2=0
    for k in keys:
        d=e.get(k,0)-f.get(k,0)
        if abs(d)>2: return None
        if d==2:p2+=1
        if d==-2:m2+=1
        rem+= [k]*max(-d,0); add+=[k]*max(d,0)
    if p2>1 or m2>1: return None
    return tuple(sorted(rem)),tuple(sorted(add))
pat=Counter(); ex={}
for p in primerange(2,N//2+1):
    for n in range(4,N+1):
        t=0;s=n
        while s%p==0: s//=p;t+=1
        if s==1: continue
        reps=allreps(n-1,p)
        for Rs,glist in reps.items():
            R=Rs*s
            if R not in reps: continue
            if any(g.get(s,0)<t for g in glist) or any(e.get(s,0)>=1 for e in reps[R]): continue
            best=None
            for g in glist:
                f=dict(g); f[s]=f.get(s,0)+1
                for e in reps[R]:
                    d=diff(f,e)
                    if d and (best is None or len(d[0])+len(d[1])<len(best[0])+len(best[1])): best=d
            # classify: removed from f (as multiples of s) and added
            key=('t=%d'%t, len(best[0]), len(best[1]))
            pat[key]+=1
            if key not in ex: ex[key]=(p,n,R,best)
for k,v in sorted(pat.items()): print(k,v,'e.g.',ex[k])
