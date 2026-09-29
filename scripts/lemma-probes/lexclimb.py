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
    reps=defaultdict(list); reps[1].append(())
    for r in U:
        nr=defaultdict(list)
        for R,lst in reps.items():
            for e in range(0,ell[r]+1):
                for d in lst: nr[R*r**e].append(d+((r,e),) if e else d)
        reps=nr
    return reps
def key(e): return sorted([r for r,c in e for _ in range(c)],reverse=True)
def adm(e,f):
    de=dict(e); df=dict(f); p2=m2=0
    for k in set(de)|set(df):
        d=df.get(k,0)-de.get(k,0)
        if abs(d)>2: return False
        if d==2:p2+=1
        if d==-2:m2+=1
    return p2<=1 and m2<=1
for m in range(3,N+1):
    for p in primerange(2,m+1):
        reps=allreps(m,p); fails=0
        for R,lst in reps.items():
            if len(lst)<2: continue
            keys=[key(e) for e in lst]
            top=max(keys)
            for i,e in enumerate(lst):
                if keys[i]==top: continue
                if not any(keys[j]>keys[i] and adm(e,lst[j]) for j in range(len(lst))):
                    fails+=1
                    if fails<=2: print('STUCK m=%d p=%d R=%d e=%s top=%s'%(m,p,R,keys[i],top))
        if fails: print('m=%d p=%d stuck=%d'%(m,p,fails),flush=True)
    print('checked',m,flush=True)
