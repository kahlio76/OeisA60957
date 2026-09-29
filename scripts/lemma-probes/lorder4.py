import sys
from sympy import primerange, isprime
from collections import defaultdict, Counter
exec(open('lorder.py').read().split('stats=Counter()')[0].split('N=int(sys.argv[1])')[1])
N=int(sys.argv[1]); stats=Counter(); ex={}
for n in range(4,N+1):
    for p in primerange(2,n//2+1):
        vals=[r for r in range(2,n+1) if r%p]
        full={}
        for r in vals:
            k=0;x=r
            while x<=n:k+=1;x*=p
            full[r]=k
        for j in range(1,max(full.values())):
            for s in [r for r in vals if full[r]>j]:
                caps={r:min(full[r], j+1 if r<s else j) for r in vals}; caps[s]=j
                reps=reps_over(caps)
                for Rs,glist in reps.items():
                    R=Rs*s
                    if R not in reps: continue
                    if any(g.get(s,0)<j for g in glist): continue
                    key=(j,isprime(s), s*s<=n, all(g.get(s*s,0)>=1 for g in glist))
                    stats[key]+=1
                    if key not in ex: ex[key]=(n,p,s,R)
    print(n,dict(stats),flush=True)
print(ex)
