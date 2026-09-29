import random, sys, itertools
from collections import defaultdict, Counter
from math import comb
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); d=int(sys.argv[3]); M=int(sys.argv[4]); MAXD=int(sys.argv[5])
def downclose(gens):
    D=set()
    for g in gens:
        for v in itertools.product(*[range(x+1) for x in g]):
            if any(v): D.add(v)
    return D
def reps(L):
    dp={tuple([0]*(d-1)):[{}]}
    for x,c in L.items():
        nd=defaultdict(list)
        for y,lst in dp.items():
            for j in range(c+1):
                y2=tuple(a+j*b for a,b in zip(y,x))
                for e in lst:
                    ee=dict(e)
                    if j: ee[x]=j
                    nd[y2].append(ee)
        dp=nd
    return dp
def lo(e): return sum(comb(c,2) for c in e.values())
st=Counter(); shown=0
for t in range(T):
    gens=[tuple(random.randint(0,M) for _ in range(d)) for _ in range(random.randint(1,4))]
    D=downclose(gens)
    if len(D)>MAXD: continue
    maxw=[w for w in D if not any(u!=w and all(a<=b for a,b in zip(w,u)) for u in D)]
    for w in maxw:
        w1=w[0]; wp=w[1:]
        if not any(wp) or w1==0: continue
        Dp=D-{w}
        L=defaultdict(int); T0=0
        for v in Dp:
            if any(v[1:]): L[v[1:]]=max(L[v[1:]],v[0]+1)
            else: T0+=v[0]
        R=reps(L)
        def hi(e): return sum(comb(L[x],2)-comb(L[x]-c,2) for x,c in e.items())
        for y,lst in R.items():
            y2=tuple(a+b for a,b in zip(y,wp))
            if y2 not in R: continue
            m=min(lo(e) for e in lst)
            mins=[e for e in lst if lo(e)==m]
            if all(e.get(wp,0)==w1 for e in mins):
                st['bad']+=1
                best=max(R[y2],key=hi)
                if hi(best)+T0 < m+w1-1: st['K2FAIL']+=1
                if shown<6:
                    shown+=1
                    print('w=%s y=%s T0=%d min=%d mins=%s best=%s hi=%d'%(w,y,T0,m,mins[:2],best,hi(best)),flush=True)
            else: st['ok']+=1
print(st)
