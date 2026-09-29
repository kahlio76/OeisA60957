import sys
from sympy import primerange
from math import comb
from collections import defaultdict
M=int(sys.argv[1])
for m in range(3,M+1):
    for p in primerange(2,m+1):
        U=[r for r in range(2,m+1) if r%p]
        ell={}
        for r in U:
            k=0; x=r
            while x<=m: k+=1; x*=p
            ell[r]=k
        k=0; x=1
        while x<=m: k+=1; x*=p
        T1=comb(k,2)
        reps={1:[(0,0)]}
        for r in U:
            nr=defaultdict(list)
            for R,ivs in reps.items():
                for e in range(0,ell[r]+1):
                    la=comb(e,2); ha=comb(ell[r],2)-comb(ell[r]-e,2)
                    for (a,b) in ivs: nr[R*r**e].append((a+la,b+ha))
            reps={R:sorted(set(v)) for R,v in nr.items()}
        strong_fail=0; weak_fail=0
        for R,ivs in reps.items():
            lomin=min(a for a,b in ivs)
            for (a,b) in ivs:
                if a>lomin:
                    # strong: every d with lower lo has a <= hd+T1+1 ; check with d = best (max hi among lo<a)
                    cands=[(a2,b2) for (a2,b2) in ivs if a2<a]
                    if not any(a<=b2+T1+1 for (a2,b2) in cands): weak_fail+=1
                    mind=[ (a2,b2) for (a2,b2) in ivs if a2==lomin]
                    if not any(a<=b2+T1+1 for (a2,b2) in mind): strong_fail+=1
        if strong_fail or weak_fail: print('m=%d p=%d strong_fail=%d weak_fail=%d'%(m,p,strong_fail,weak_fail),flush=True)
    if m%5==0: print('checked',m,flush=True)
