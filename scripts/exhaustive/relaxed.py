import sys
from sympy import primerange
from math import comb
from collections import defaultdict
M0=int(sys.argv[1]); M=int(sys.argv[2])
def admissible(e,f):
    plus2=0; minus2=0
    for a,b in zip(e,f):
        d=b-a
        if d>2 or d<-2: return False
        if d==2: plus2+=1
        if d==-2: minus2+=1
    return plus2<=1 and minus2<=1
for m in range(M0,M+1):
    for p in primerange(2,m+1):
        U=[r for r in range(2,m+1) if r%p]
        ell={}
        for r in U:
            k=0;x=r
            while x<=m: k+=1;x*=p
            ell[r]=k
        reps=defaultdict(list); reps[1].append(())
        for r in U:
            nr=defaultdict(list)
            for R,lst in reps.items():
                for e in range(0,ell[r]+1):
                    for t in lst: nr[R*r**e].append(t+(e,))
            reps=nr
        bad=0; big=0
        for R,lst in reps.items():
            n=len(lst)
            if n==1: continue
            big=max(big,n)
            seen={0}; st=[0]
            while st:
                i=st.pop()
                for j in range(n):
                    if j not in seen and admissible(lst[i],lst[j]): seen.add(j); st.append(j)
            if len(seen)!=n:
                bad+=1
                if bad<=2: print('  DISCONNECTED m=%d p=%d R=%d nreps=%d'%(m,p,R,n))
        if bad: print('m=%d p=%d disconnectedR=%d'%(m,p,bad),flush=True)
    print('checked',m,flush=True)
