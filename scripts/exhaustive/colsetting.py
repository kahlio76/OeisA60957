import sys
from sympy import primerange, divisors
from collections import defaultdict, Counter
N0=int(sys.argv[1]); N=int(sys.argv[2])
def madj(e,f):
    pos=[e.get(k,0)-f.get(k,0) for k in set(e)|set(f)]
    return sum(1 for v in pos if v>=2)<=1 and sum(1 for v in pos if v<=-2)<=1
st=Counter()
for n in range(N0,N+1):
  for p in primerange(2,n+1):
    L=lambda s: (lambda k: k)(sum(1 for i in range(40) if s*p**i<=n))
    P=[s for s in range(2,n+1) if s%p]
    for x in P:
        if all(x%d for d in range(2,x)): continue
        W=[s for s in P if s<x]
        reps=defaultdict(list); reps[1].append({})
        for s in W:
            nr=defaultdict(list)
            for R,lst in reps.items():
                for j in range(L(s)+1):
                    for e in lst:
                        if j: ee=dict(e); ee[s]=j
                        else: ee=e
                        nr[R*s**j].append(ee)
            reps=nr
        for Nv in list(reps):
            # Lemma L
            ts=[t for t in range(0,6) if Nv*x**t in reps]
            if ts!=list(range(len(ts))): st['LFAIL']+=1; print('LFAIL',n,p,x,Nv,ts)
            if Nv*x in reps:
                F=reps[Nv]; E=reps[Nv*x]
                simple=False
                for f in F:
                    for d in divisors(x):
                        if 1<d<x and d<=x//d:
                            g=dict(f); g[d]=g.get(d,0)+1; g[x//d]=g.get(x//d,0)+1
                            if all(g[k]<=L(k) for k in (d,x//d)): simple=True;break
                    if simple: break
                if simple: st['simple']+=1; continue
                ok=any(madj(dict(f,**{}) ,e) for f in F for e in E) # placeholder
                # proper check: f + x vs e
                ok=False
                for f in F:
                    fx=dict(f); fx[x]=1
                    if any(madj(fx,e) for e in E): ok=True;break
                st['exch' if ok else 'BRFAIL']+=1
                if not ok: print('BRFAIL',n,p,x,Nv,flush=True)
  print('done',n,dict(st),flush=True)
