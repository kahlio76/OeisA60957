import random, sys
exec(open('allbad.py').read().split('stat=Counter()')[0])
shown=0
for trial in range(T):
    gens=random.sample(range(2,50),random.randint(2,5))
    V=set()
    for g in gens: V|=set(d for d in divisors(g) if d>1)
    cap={v:(random.choice([2,3]) if random.random()<0.25 else 1) for v in V}
    full=reps(V,cap)
    for R,lst in full.items():
        cands=[s for s in V if cap[s]>=2 and R%s==0]
        if not cands or len(lst)<2: continue
        for s in cands:
          if s*s in V: continue
          if set(e.get(s,0) for e in lst)=={0,cap[s]}:
            if shown<6:
                shown+=1
                print('s=%d cap=%s R=%d V=%s'%(s,cap[s],R,sorted(V)))
                for e in lst[:6]: print('   ',e)
