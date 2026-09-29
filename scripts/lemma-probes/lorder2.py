import sys
from sympy import primerange, isprime
from collections import defaultdict, Counter
N=int(sys.argv[1])
exec(open('lorder.py').read().split('stats=Counter()')[0].split('N=int(sys.argv[1])')[1])
def diff(f,e):
    keys=set(f)|set(e); rem=[];add=[]
    for k in keys:
        d=e.get(k,0)-f.get(k,0)
        rem+=[k]*max(-d,0); add+=[k]*max(d,0)
    return tuple(sorted(rem)),tuple(sorted(add))
stats=Counter(); ex={}
for n in range(4,N+1):
    for p in primerange(2,n+1):
        vals=[r for r in range(2,n+1) if r%p]
        full={}
        for r in vals:
            k=0;x=r
            while x<=n:k+=1;x*=p
            full[r]=k
        maxl=max(full.values())
        for j in range(1,maxl):
            for s in [r for r in vals if full[r]>j]:
                caps={r:min(full[r], j+1 if r<s else j) for r in vals}; caps[s]=j
                reps=reps_over(caps)
                for Rs,glist in reps.items():
                    R=Rs*s
                    if R not in reps: continue
                    O=reps[R]
                    if any(e.get(s,0)>=1 for e in O) or any(g.get(s,0)<j for g in glist): continue
                    best=None
                    for g in glist:
                        f=dict(g); f[s]=f.get(s,0)+1
                        for e in O:
                            if adm(f,e):
                                d=diff(f,e)
                                if best is None or len(d[0])+len(d[1])<len(best[0])+len(best[1]): best=d
                    key=(j, 'prime' if isprime(s) else 'comp', 's2<=n' if s*s<=n else 's2>n', len(best[0]),len(best[1]))
                    stats[key]+=1
                    if key not in ex: ex[key]=(n,p,s,R,best)
for k,v in sorted(stats.items()): print(k,v,'e.g.',ex[k])
