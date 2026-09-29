import sys
from sympy import primerange
from math import comb
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
def lo(e): return sum(comb(c,2) for r,c in e)
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
        reps=allreps(m,p); h1=0; h2=0
        for R,lst in reps.items():
            los=[lo(e) for e in lst]; lmin=min(los)
            for e,l in zip(lst,los):
                if l>lmin and not any(lo(f)<l and adm(e,f) for f in lst):
                    h1+=1
                    if h1<=2: print('H1 FAIL m=%d p=%d R=%d e=%s lo=%d lmin=%d'%(m,p,R,e,l,lmin))
            mins=[e for e,l in zip(lst,los) if l==lmin]
            if lmin>=2 and len(mins)>1:
                # connectivity among mins via admissible direct edges only
                seen={0}; st=[0]
                while st:
                    i=st.pop()
                    for j in range(len(mins)):
                        if j not in seen and adm(mins[i],mins[j]): seen.add(j); st.append(j)
                if len(seen)<len(mins):
                    h2+=1
                    if h2<=2: print('H2 FAIL m=%d p=%d R=%d mins=%s'%(m,p,R,mins[:4]))
        if h1 or h2: print('m=%d p=%d H1fail=%d H2fail=%d'%(m,p,h1,h2),flush=True)
    print('checked',m,flush=True)
