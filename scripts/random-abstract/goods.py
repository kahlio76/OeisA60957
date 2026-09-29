import random, sys
from sympy import divisors
from collections import defaultdict
random.seed(int(sys.argv[1])); T=int(sys.argv[2])
def reps(V,cap):
    dp=defaultdict(list); dp[1].append({})
    for v in sorted(V):
        c=cap[v]
        nd=defaultdict(list)
        for R,lst in dp.items():
            for k in range(0,c+1):
                for d in lst:
                    dd=dict(d)
                    if k: dd[v]=k
                    nd[R*v**k].append(dd)
        dp=nd
    return dp
nobad=0; tot=0
for trial in range(T):
    gens=random.sample(range(2,40),random.randint(2,4))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    cap={v:random.randint(1,3) for v in V}
    full=reps(V,cap)
    for R in full:
        cands=[s for s in V if cap[s]>=2]
        if not cands: continue
        tot+=1
        good=False
        for s in cands:
            c=dict(cap); c[s]-=1
            rr=reps(V,c) if False else None
            # compute reps under c restricted: filter full reps
            RepR=[e for e in full[R] if e.get(s,0)<=c[s]]
            if R%s: good=True;break
            RepRs=[e for e in full.get(R//s,[]) if e.get(s,0)<=c[s]]
            if not RepR or not RepRs: good=True;break
            if any(g.get(s,0)<c[s] for g in RepRs): good=True;break
        if not good:
            nobad+=1
            if nobad<=3: print('NO GOOD s: V=%s cap=%s R=%d'%(sorted(V),cap,R))
print('classes',tot,'without good s',nobad)
