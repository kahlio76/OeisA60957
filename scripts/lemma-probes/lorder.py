import sys
from sympy import primerange
from collections import defaultdict, Counter
N=int(sys.argv[1])
def reps_over(caps):
    reps=defaultdict(list); reps[1].append({})
    for r,c in caps.items():
        if c==0: continue
        nr=defaultdict(list)
        for R,lst in reps.items():
            for e in range(0,c+1):
                for d in lst:
                    dd=dict(d)
                    if e: dd[r]=e
                    nr[R*r**e].append(dd)
        reps=nr
    return reps
def adm(f,e):
    keys=set(f)|set(e); p2=m2=0
    for k in keys:
        d=e.get(k,0)-f.get(k,0)
        if abs(d)>2: return False
        if d==2:p2+=1
        if d==-2:m2+=1
    return p2<=1 and m2<=1
stats=Counter()
for n in range(4,N+1):
    for p in primerange(2,n+1):
        vals=[r for r in range(2,n+1) if r%p]
        full={}
        for r in vals:
            k=0;x=r
            while x<=n:k+=1;x*=p
            full[r]=k
        maxl=max(full.values())
        for j in range(1,maxl):        # level j additions (t=j)
            for s in [r for r in vals if full[r]>j]:
                caps={r:min(full[r], j+1 if r<s else j) for r in vals}
                caps[s]=j
                reps=reps_over(caps)
                for Rs,glist in reps.items():
                    R=Rs*s
                    if R not in reps: continue
                    O=reps[R]
                    if any(e.get(s,0)>=1 for e in O) or any(g.get(s,0)<j for g in glist): continue
                    ok=False
                    for g in glist:
                        f=dict(g); f[s]=f.get(s,0)+1
                        if any(adm(f,e) for e in O): ok=True;break
                    stats[('bad', ok)]+=1
                    if stats[('bad',ok)]<=3: print('BAD n=%d p=%d s=%d t=%d R=%d bridged=%s'%(n,p,s,j,R,ok))
    if n%4==0: print('n',n,dict(stats),flush=True)
print(dict(stats))
