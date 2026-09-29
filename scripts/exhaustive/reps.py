import sys
from sympy import primerange
from math import comb
from collections import defaultdict
M=int(sys.argv[1])
def chains(m,p):
    U=[r for r in range(1,m+1) if r%p]
    ell={}
    for r in U:
        k=0; x=r
        while x<=m: k+=1; x*=p
        ell[r]=k
    return U,ell
for m in range(2,M+1):
    for p in primerange(2,m+1):
        U,ell=chains(m,p)
        # enumerate reps via DP over parts: state R -> list of (lo,hi) pairs (can be many) ; keep extremes: min lo with its max hi, max hi with its min lo, and all intervals for union check
        reps={1:[(0,0)]}
        for r in U:
            nr=defaultdict(list)
            for R,ivs in reps.items():
                for e in range(0,ell[r]+1):
                    lo_add=comb(e,2); hi_add=comb(ell[r],2)-comb(ell[r]-e,2)
                    RR=R*r**e
                    for (a,b) in ivs: nr[RR].append((a+lo_add,b+hi_add))
            # prune: keep for each R the union-relevant intervals (dedupe)
            reps={R:sorted(set(v)) for R,v in nr.items()}
        bad2=0; badU=0
        for R,ivs in reps.items():
            ivs.sort()
            # union connectivity
            cur=ivs[0][1]; ok=True
            for a,b in ivs[1:]:
                if a>cur+1: ok=False
                cur=max(cur,b)
            if not ok: badU+=1
            A=min(a for a,b in ivs); B=max(b for a,b in ivs)
            emin_hi=max(b for a,b in ivs if a==A); emax_lo=min(a for a,b in ivs if b==B)
            if emax_lo>emin_hi+1: bad2+=1
        if badU or bad2: print('m=%d p=%d unionBad=%d twoRepFail=%d'%(m,p,badU,bad2),flush=True)
    if m%5==0: print('checked',m,flush=True)
