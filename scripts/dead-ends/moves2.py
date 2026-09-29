import sys
from sympy import primerange, divisors
from math import comb
from collections import defaultdict
M=int(sys.argv[1])
def reps_of(U,ell):
    reps=defaultdict(list); reps[1].append(())
    for r in U:
        nr=defaultdict(list)
        for R,lst in reps.items():
            for e in range(0,ell[r]+1):
                RR=R*r**e
                for t in lst: nr[RR].append(t+(e,))
        reps=nr
    return reps
for m in range(4,M+1):
    for p in primerange(2,m+1):
        U=[r for r in range(2,m+1) if r%p]; idx={r:i for i,r in enumerate(U)}
        ell={}
        for r in U:
            k=0;x=r
            while x<=m: k+=1;x*=p
            ell[r]=k
        k=0;x=1
        while x<=m:k+=1;x*=p
        T1=comb(k,2)
        reps=reps_of(U,ell)
        p1fail=0; p2fail=0
        for R,lst in reps.items():
            S=set(lst)
            def J(e): return (sum(comb(c,2) for c in e), sum(comb(ell[r],2)-comb(ell[r]-e[idx[r]],2) for r in U)+T1)
            # build graph via split moves
            adj=defaultdict(list)
            for e in lst:
                for r in U:
                    if e[idx[r]]==0: continue
                    for a in divisors(r):
                        b=r//a
                        if a<2 or b<2 or a>b: continue
                        f=list(e); f[idx[r]]-=1; f[idx[a]]+=1; f[idx[b]]+=1
                        f=tuple(f)
                        if f in S:
                            adj[e].append(f); adj[f].append(e)
                            (l1,h1),(l2,h2)=J(e),J(f)
                            if l2>h1+1 or l1>h2+1: p1fail+=1
            # connectivity
            seen={lst[0]}; st=[lst[0]]
            while st:
                u=st.pop()
                for w in adj[u]:
                    if w not in seen: seen.add(w); st.append(w)
            if len(seen)!=len(S): p2fail+=1
        if p1fail or p2fail: print('m=%d p=%d P1fail=%d P2fail(disconnected R)=%d'%(m,p,p1fail,p2fail),flush=True)
    print('checked',m,flush=True)
