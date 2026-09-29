import sys
from sympy import primerange
from math import comb
from collections import defaultdict
from itertools import combinations_with_replacement as cwr
def analyze(m,p,MAXK=2,show=3):
    U=[r for r in range(2,m+1) if r%p]; idx={r:i for i,r in enumerate(U)}
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
    byprod=defaultdict(list)
    for s in range(1,MAXK+1):
        for X in cwr(U,s):
            pr=1
            for x in X: pr*=x
            byprod[pr].append(X)
    out=0
    for R,lst in reps.items():
        S=set(lst); adj=defaultdict(set)
        for e in lst:
            present=[r for r in U if e[idx[r]]>0]
            for s in range(1,MAXK+1):
                for X in cwr(present,s):
                    cnt=defaultdict(int)
                    for x in X: cnt[x]+=1
                    if any(cnt[x]>e[idx[x]] for x in cnt): continue
                    pr=1
                    for x in X: pr*=x
                    for Y in byprod[pr]:
                        f=list(e)
                        for x in X: f[idx[x]]-=1
                        for y in Y: f[idx[y]]+=1
                        f=tuple(f)
                        if f in S and f!=e: adj[e].add(f); adj[f].add(e)
        comps=[]; seen=set()
        for e in lst:
            if e in seen: continue
            c=[e]; seen.add(e); st=[e]
            while st:
                u=st.pop()
                for w in adj[u]:
                    if w not in seen: seen.add(w); st.append(w); c.append(w)
            comps.append(c)
        if len(comps)>1 and out<show:
            out+=1
            print('m=%d p=%d R=%d components:'%(m,p,R))
            for c in comps:
                print('   ',[ {r:e[idx[r]] for r in U if e[idx[r]]} for e in c][:4])
analyze(9,5); analyze(11,7); analyze(11,11)
