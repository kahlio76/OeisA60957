import random, sys, itertools
from collections import defaultdict
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); d=int(sys.argv[3]); M=int(sys.argv[4]); C=int(sys.argv[5])
def downclose(gens):
    D=set()
    for g in gens:
        for v in itertools.product(*[range(x+1) for x in g]):
            if any(v): D.add(v)
    return D
dirsl=[v for v in itertools.product(range(-2,3),repeat=d) if any(v) and next(x for x in v if x)>0]
from collections import Counter
bad=Counter()
for t in range(T):
    gens=[tuple(random.randint(0,M) for _ in range(d)) for _ in range(random.randint(1,3))]
    W=sorted(downclose(gens))
    if len(W)>14: continue
    cap={v:random.randint(1,C) for v in W}
    S={tuple([0]*d)}
    for v in W:
        S={tuple(s[i]+j*v[i] for i in range(d)) for s in S for j in range(cap[v]+1)}
    for dv in dirsl:
        for s in S:
            # find next point along dv beyond gap
            k=1
            while tuple(s[i]+k*dv[i] for i in range(d)) not in S and k<40: k+=1
            if 1<k<40:
                # s in S, s+k dv in S, intermediate missing: hole
                bad[dv]+=1
                if bad[dv]==1: print('HOLE dir',dv,W,cap,s,k,flush=True)
                break
print(dict(bad))
