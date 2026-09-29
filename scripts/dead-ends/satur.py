import random, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); d=int(sys.argv[3]); M=int(sys.argv[4]); C=int(sys.argv[5])
def downclose(gens):
    D=set()
    for g in gens:
        for v in itertools.product(*[range(x+1) for x in g]):
            if any(v): D.add(v)
    return D
bad=0
for t in range(T):
    gens=[tuple(random.randint(0,M) for _ in range(d)) for _ in range(random.randint(1,3))]
    W=sorted(downclose(gens))
    if len(W)>12: continue
    cap={v:random.randint(1,C) for v in W}
    S={tuple([0]*d)}
    for v in W:
        S={tuple(s[i]+j*v[i] for i in range(d)) for s in S for j in range(cap[v]+1)}
    pts=np.array(sorted(S))
    # check lattice points in hull
    dims=[i for i in range(d) if pts[:,i].max()>0]
    P=pts[:,dims]
    if len(dims)<d or len(P)<=len(dims): continue
    try: H=ConvexHull(P)
    except Exception: continue
    ranges=[range(int(P[:,i].max())+1) for i in range(len(dims))]
    Sset=set(map(tuple,P))
    for q in itertools.product(*ranges):
        if q in Sset: continue
        if all(np.dot(eq[:-1],q)+eq[-1]<=1e-9 for eq in H.equations):
            bad+=1
            if bad<=5: print('HOLE',W,cap,q,flush=True)
            break
print('bad',bad)
