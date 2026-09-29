import sys
from sympy import primerange
from collections import defaultdict, Counter
exec(open('lorder.py').read().split('stats=Counter()')[0].split('N=int(sys.argv[1])')[1])
N=int(sys.argv[1]); mode=sys.argv[2]
stats=Counter()
for n in range(4,N+1):
    for p in primerange(2,n//2+1):
        vals=[r for r in range(2,n+1) if r%p]
        full={}
        for r in vals:
            k=0;x=r
            while x<=n:k+=1;x*=p
            full[r]=k
        order=[]
        for j in range(max(full.values())):
            lv=[r for r in vals if full[r]>j]
            if mode=='dec': lv=lv[::-1]
            order+= [(j,r) for r in lv]
        caps={r:0 for r in vals}
        for (j,s) in order:
            if j==0: caps[s]=1; continue
            reps=reps_over(caps)
            for Rs,glist in reps.items():
                R=Rs*s
                if R not in reps: continue
                if any(g.get(s,0)<j for g in glist): continue
                stats['bad j=%d'%j]+=1
            caps[s]=j+1
    print(n,mode,dict(stats),flush=True)
