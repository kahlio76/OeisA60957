import sys
from sympy import primerange
from math import comb
from collections import defaultdict
from itertools import combinations_with_replacement as cwr
M=int(sys.argv[1]); MAXK=int(sys.argv[2])  # moves: replace multiset X (|X|<=MAXK) by Y (|Y|<=MAXK) with same product
def reps_of(U,ell):
    reps=defaultdict(list); reps[1].append(())
    for r in U:
        nr=defaultdict(list)
        for R,lst in reps.items():
            for e in range(0,ell[r]+1):
                for t in lst: nr[R*r**e].append(t+(e,))
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
        # precompute small multisets by product
        byprod=defaultdict(list)
        for s in range(1,MAXK+1):
            for X in cwr(U,s):
                pr=1
                for x in X: pr*=x
                byprod[pr].append(X)
        reps=reps_of(U,ell)
        p1fail=0; p2fail=0
        for R,lst in reps.items():
            S=set(lst)
            def J(e): return (sum(comb(c,2) for c in e), sum(comb(ell[r],2)-comb(ell[r]-e[idx[r]],2) for r in U)+T1)
            adj=defaultdict(set)
            for e in lst:
                # choose sub-multiset X of e with |X|<=MAXK, replace by Y with same product
                parts=[r for r in U for _ in range(e[idx[r]])]
                for s in range(1,MAXK+1):
                    for X in set(cwr(sorted(set(parts)),s)):
                        cnt=defaultdict(int)
                        for x in X: cnt[x]+=1
                        if any(cnt[x]>e[idx[x]] for x in cnt): continue
                        pr=1
                        for x in X: pr*=x
                        for Y in byprod[pr]:
                            if Y==X: continue
                            f=list(e)
                            for x in X: f[idx[x]]-=1
                            for y in Y: f[idx[y]]+=1
                            f=tuple(f)
                            if f in S and f not in adj[e]:
                                adj[e].add(f); adj[f].add(e)
                                (l1,h1),(l2,h2)=J(e),J(f)
                                if l2>h1+1 or l1>h2+1: p1fail+=1
            seen={lst[0]}; st=[lst[0]]
            while st:
                u=st.pop()
                for w in adj[u]:
                    if w not in seen: seen.add(w); st.append(w)
            if len(seen)!=len(S): p2fail+=1
        if p1fail or p2fail: print('m=%d p=%d P1fail=%d P2fail=%d'%(m,p,p1fail,p2fail),flush=True)
    print('checked',m,flush=True)
