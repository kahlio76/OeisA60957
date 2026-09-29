import random, sys
from sympy import divisors
from collections import defaultdict, Counter
exec(open('badres.py').read().split('random.seed')[0].split('exec(')[0])
exec('def reps'+open('badres.py').read().split('def reps')[1].split('random.seed')[0])
random.seed(int(sys.argv[1])); T=int(sys.argv[2])
st=Counter()
for trial in range(T):
    gens=random.sample(range(2,40),random.randint(2,4))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    cap={v:(random.choice([2,3]) if random.random()<0.4 else 1) for v in V}
    full=reps(V,cap)
    maxs=[s for s in V if not any(m!=s and m%s==0 for m in V)]
    for R,lst in full.items():
        for s in maxs:
            if cap[s]<2 or R%s: continue
            k=cap[s]-1
            Rs=[e for e in full.get(R//s,[]) if e.get(s,0)<=k]
            if not Rs or all(e.get(s,0)>=1 for e in lst): st['trivial']+=1; continue
            if any(g.get(s,0)<k for g in Rs): st['good']+=1; continue
            st['BAD']+=1
            if st['BAD']<=3: print('BAD s=%d R=%d V=%s cap=%s'%(s,R,sorted(V),cap), lst[:5])
print(st)
