import random, sys
from math import comb
from sympy import divisors
from collections import defaultdict, Counter
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
stat=Counter(); shown=0
for trial in range(T):
    gens=random.sample(range(2,50),random.randint(2,5))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    cap={v:(random.choice([2,3]) if random.random()<0.25 else 1) for v in V}
    full=reps(V,cap)
    for R,lst in full.items():
        cands=[s for s in V if cap[s]>=2 and R%s==0]
        if not cands or len(lst)<2: continue
        allbad=all(set(e.get(s,0) for e in lst)=={0,cap[s]} for s in cands)
        if allbad:
            # describe: caps of cands, whether s^2 in V
            desc=tuple(sorted((cap[s], s*s in V) for s in cands))
            stat[desc]+=1
            if shown<8:
                shown+=1
                print('ALLBAD R=%d cands=%s caps=%s reps=%s'%(R,cands,{s:cap[s] for s in cands},lst[:4]))
print(stat.most_common(10))
