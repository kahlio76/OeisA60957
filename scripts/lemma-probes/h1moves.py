import sys
from sympy import primerange
from math import comb
from collections import defaultdict, Counter
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
    return reps,ell
def lo(e): return sum(comb(c,2) for r,c in e)
def diff(e,f):
    de=dict(e); df=dict(f); rem=[];add=[];p2=m2=0
    for k in set(de)|set(df):
        d=df.get(k,0)-de.get(k,0)
        if abs(d)>2: return None
        if d==2:p2+=1
        if d==-2:m2+=1
        rem+=[k]*max(-d,0); add+=[k]*max(d,0)
    if p2>1 or m2>1: return None
    return tuple(sorted(rem)),tuple(sorted(add))
pat=Counter(); ex={}
for m in range(3,N+1):
    for p in primerange(2,m+1):
        reps,ell=allreps(m,p)
        for R,lst in reps.items():
            los=[lo(e) for e in lst]; lmin=min(los)
            for e,l in zip(lst,los):
                if l==lmin: continue
                best=None
                for f in lst:
                    if lo(f)<l:
                        d=diff(e,f)
                        if d and (best is None or len(d[0])+len(d[1])<len(best[0])+len(best[1])): best=d
                # classify shape: does removed contain a repeated value r (x2)? relation type
                rem,add=best
                cr=Counter(rem)
                shape='rem%d add%d'%(len(rem),len(add))
                if any(c==2 for c in cr.values()): shape+=' remdouble'
                pat[shape]+=1
                if shape not in ex: ex[shape]=(m,p,R,dict(e),best)
for k,v in pat.most_common(): print(v,k,'e.g.',ex[k])
