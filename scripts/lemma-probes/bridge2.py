import sys
from sympy import primerange
from collections import defaultdict
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
def adm(f,e):
    keys=set(f)|set(e); p2=m2=0; size=0
    for k in keys:
        d=e.get(k,0)-f.get(k,0)
        if abs(d)>2: return None
        if d==2:p2+=1
        if d==-2:m2+=1
        size+=abs(d)
    if p2>1 or m2>1: return None
    return size
for p in primerange(2,N//2+1):
    hist=defaultdict(int); fails=0
    for n in range(4,N+1):
        t=0;s=n
        while s%p==0: s//=p; t+=1
        if s==1: continue
        reps=allreps(n-1,p)
        for Rs,glist in reps.items():
            R=Rs*s
            if R not in reps: continue
            if any(g.get(s,0)<t for g in glist): continue
            best=None
            for g in glist:
                f=dict(g); f[s]=f.get(s,0)+1
                for e in reps[R]:
                    z=adm(f,e)
                    if z is not None and (best is None or z<best[0]): best=(z,f,e)
            if best is None:
                fails+=1
                if fails<=3: print('NO BRIDGE p=%d n=%d R=%d'%(p,n,R))
            else: hist[best[0]]+=1
    print('p=%d bridge-size histogram %s fails %d'%(p,dict(sorted(hist.items())),fails),flush=True)
