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
def inK(e):
    doubles=[c for r,c in e if c>=2]
    return len(doubles)==0 or (len(doubles)==1 and doubles[0]==2)
def excess(e): return sum(max(c-1,0) for r,c in e)+ (0 if inK(e) else 1)
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
        reps=allreps(m,p); stuck=0; noK=0
        for R,lst in reps.items():
            if not any(inK(e) for e in lst): noK+=1
            for e in lst:
                if inK(e): continue
                if not any(excess(f)<excess(e) and adm(e,f) for f in lst):
                    stuck+=1
                    if stuck<=2: print('STUCK m=%d p=%d R=%d e=%s'%(m,p,R,e))
        if stuck or noK: print('m=%d p=%d stuck=%d classes_without_K=%d'%(m,p,stuck,noK),flush=True)
    print('checked',m,flush=True)
