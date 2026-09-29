import sys
from sympy import primerange, divisors
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
    return reps,ell
for p in primerange(2,N//2+1):
    fails=defaultdict(int)
    for n in range(4,N+1):
        t=0;s=n
        while s%p==0: s//=p; t+=1
        if s==1: continue
        reps,ell=allreps(n-1,p)
        cap=lambda r: ell.get(r,0)
        for Rs,glist in reps.items():
            R=Rs*s
            if R not in reps: continue
            if any(g.get(s,0)<t for g in glist): continue   # not bad
            ok=False
            for g in glist:
                # S1: split s=a*b with room
                for a in divisors(s):
                    b=s//a
                    if a<2 or b<2 or a>b: continue
                    if a==b:
                        if g.get(a,0)+2<=cap(a): ok=True
                    elif g.get(a,0)+1<=cap(a) and g.get(b,0)+1<=cap(b): ok=True
                    if ok: break
                if ok: break
                # S3 merge s with existing part k: sk<=n-1, room at sk ; and for t>=1 need: f=g+s ; e=g-k+sk
                for k in list(g.keys()):
                    if s*k<=n-1 and g.get(s*k,0)+1<=cap(s*k): ok=True; break
                if ok: break
                # S2 (s repeated): e = g - s + s^2 (merge two s into s^2) : f=g+s has t+1 copies
                if g.get(s,0)>=1 and s*s<=n-1 and g.get(s*s,0)+1<=cap(s*s): ok=True; break
            if not ok:
                fails[(t,s==n)]+=1
                if fails[(t,s==n)]<=3: print('UNBRIDGED p=%d n=%d s=%d t=%d R=%d g=%s'%(p,n,s,t,R,glist[:2]))
    print('p=%d fails=%s'%(p,dict(fails)),flush=True)
