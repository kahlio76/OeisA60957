import sys
from sympy import primerange
from collections import defaultdict, Counter
exec('def allreps'+open('realbad.py').read().split('def allreps')[1].split('st=Counter()')[0])
N0=int(sys.argv[1]); N=int(sys.argv[2])
st=Counter(); ex={}
def madj(e,f):
    keys=set(e)|set(f)
    pos=[e.get(k,0)-f.get(k,0) for k in keys]
    return sum(1 for x in pos if x>=2)<=1 and sum(1 for x in pos if x<=-2)<=1
for n in range(N0,N+1):
    for p in primerange(2,n):
        r=n;k=0
        while r%p==0: r//=p;k+=1
        if r==1: continue
        reps,ell=allreps(n-1,p)
        for A,lst in reps.items():
            if A*r not in reps: continue
            if any(e.get(r,0)<k for e in lst): continue
            Xs=reps[A*r]
            best=None
            for Q in lst:
                Z=dict(Q); Z[r]=Z.get(r,0)+1
                for X in Xs:
                    if madj(Z,X):
                        dp={s:X.get(s,0)-Z.get(s,0) for s in set(X)|set(Z)}
                        plus=tuple(sorted((s,c) for s,c in dp.items() if c>0 and s!=r))
                        minus=tuple(sorted((s,-c) for s,c in dp.items() if c<0 and s!=r))
                        sz=sum(c for s,c in plus)+sum(c for s,c in minus)
                        if best is None or sz<best[0]: best=(sz,plus,minus)
            if best is None:
                st['NOBRIDGE']+=1; print('NOBRIDGE n=%d p=%d r=%d k=%d A=%d'%(n,p,r,k,A),flush=True)
            else:
                # pattern: express in terms of r
                key=(k>0,best[0],len(best[1]),len(best[2]))
                st[key]+=1
                if key not in ex: ex[key]=(n,p,r,k,A,best)
    print('done',n,flush=True)
for k,v in sorted(st.items(),key=str): print(k,v,ex.get(k))
